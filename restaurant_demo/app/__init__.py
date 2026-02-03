from flask import Flask, render_template, redirect, url_for, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    
    from config import Config
    app.config.from_object(Config)
    
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    # Auto-seed for Vercel/Demo mode
    with app.app_context():
        is_memory = str(app.config.get('SQLALCHEMY_DATABASE_URI', '')).startswith('sqlite:///:memory:')
        if is_memory or os.environ.get('VERCEL') or os.environ.get('DEMO_MODE'):
            from .seeds import seed_data
            seed_data()
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicie sesión para continuar.'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import Usuario
        return db.session.get(Usuario, int(user_id))
    
    from .blueprints.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from .blueprints.menu import menu_bp
    app.register_blueprint(menu_bp, url_prefix='/menu')
    
    from .blueprints.pedidos import pedidos_bp
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    
    @app.before_request
    def require_login():
        allowed_routes = ['auth.login', 'auth.logout', 'static', 'health_check']
        if request.endpoint and request.endpoint not in allowed_routes:
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
    
    @app.context_processor
    def inject_now():
        from datetime import date
        return {'now': date.today()}
    
    @app.route('/')
    def index():
        from .models import Pedido, Estado
        from datetime import date, datetime
        
        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        
        pedidos_hoy = Pedido.query.filter(Pedido.fecha >= start_of_day).all()
        pedidos_count = len(pedidos_hoy)
        
        estados_stats = {}
        for p in pedidos_hoy:
            nombre_estado = p.estado.nombre if p.estado else 'Sin Estado'
            estados_stats[nombre_estado] = estados_stats.get(nombre_estado, 0) + 1
        
        pedidos_activos = Pedido.query.join(Estado).filter(
            Estado.is_final == False
        ).count()
        
        ultimos_pedidos = Pedido.query.order_by(Pedido.fecha.desc()).limit(5).all()
        
        return render_template('index.html',
                             pedidos_count=pedidos_count,
                             estados_stats=estados_stats,
                             pedidos_activos=pedidos_activos,
                             ultimos_pedidos=ultimos_pedidos)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return render_template('errors/500.html'), 500
    
    @app.route('/health')
    def health_check():
        from flask import jsonify
        from sqlalchemy import text
        try:
            db.session.execute(text('SELECT 1'))
            return jsonify({'status': 'healthy', 'database': 'connected'}), 200
        except Exception:
            return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 503
    
    return app
