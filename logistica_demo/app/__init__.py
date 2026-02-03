from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from sqlalchemy import text
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    from config import Config
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    
    # Auto-initialize DB for Demo/Vercel (if using in-memory)
    with app.app_context():
        if ':memory:' in app.config['SQLALCHEMY_DATABASE_URI']:
            # Import models so create_all knows about them
            from .models import Usuario, Cliente, Producto, Chofer, Vehiculo, Estado, Pedido, Envio
            db.create_all()
            from .demo_data import init_demo_data
            init_demo_data()
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
    from .blueprints.pedidos import pedidos_bp
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    from .blueprints.recursos import recursos_bp
    app.register_blueprint(recursos_bp, url_prefix='/recursos')
    from .blueprints.envios import envios_bp
    app.register_blueprint(envios_bp, url_prefix='/envios')

    @app.before_request
    def require_login():
        allowed_routes = ['auth.login', 'auth.logout', 'static', 'health_check']
        if request.endpoint and request.endpoint not in allowed_routes:
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))

    @app.context_processor
    def inject_globals():
        from datetime import date, timedelta
        return {'now': date.today(), 'timedelta': timedelta}
    _alertas_cache = {'data': None, 'timestamp': None}

    def get_alertas_documentacion():
        from .models import Chofer, Vehiculo
        from datetime import datetime, timedelta
        cache_duration = timedelta(minutes=5)
        now = datetime.now()
        if _alertas_cache['data'] is not None and _alertas_cache['timestamp'] and (now - _alertas_cache['timestamp'] < cache_duration):
            return _alertas_cache['data']
        alertas = {'Chofer': [], 'Vehículo': []}
        for c in Chofer.query.all():
            estado = c.estado_documentacion
            if estado['global_status'] in ['danger', 'warning']:
                alertas['Chofer'].append({'nombre': f'{c.nombre} {c.apellido}', 'status': estado['global_status'], 'alertas': estado['alertas'], 'avisos': estado['avisos']})
        for v in Vehiculo.query.all():
            estado = v.estado_documentacion
            if estado['global_status'] in ['danger', 'warning']:
                alertas['Vehículo'].append({'nombre': f'{v.patente}', 'status': estado['global_status'], 'alertas': estado['alertas'], 'avisos': estado['avisos']})
        alertas = {k: v for k, v in alertas.items() if v}
        _alertas_cache['data'] = alertas
        _alertas_cache['timestamp'] = now
        return alertas

    @app.route('/')
    def index():
        from .models import Pedido, Envio, Estado
        from datetime import date, datetime
        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        pedidos_hoy = Pedido.query.filter(Pedido.fecha >= start_of_day).count()
        envios_activos = Envio.query.join(Estado).filter(Estado.is_final == False).count()
        ultimos_pedidos = Pedido.query.order_by(Pedido.fecha.desc()).limit(5).all()
        alertas = get_alertas_documentacion()
        return render_template('index.html', pedidos_hoy=pedidos_hoy, envios_activos=envios_activos, ultimos_pedidos=ultimos_pedidos, alertas=alertas)

    @app.errorhandler(404)
    def page_not_found(e):
        return (render_template('errors/404.html'), 404)

    @app.errorhandler(500)
    def internal_error(e):
        return (render_template('errors/500.html'), 500)

    @app.route('/health')
    def health_check():
        try:
            db.session.execute(text('SELECT 1'))
            return (jsonify({'status': 'healthy', 'database': 'connected'}), 200)
        except Exception:
            return (jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 503)
    return app