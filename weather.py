import os

from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import Day, Hour, Locality
from app.weather import weather_factory
from app.weather.base import WeatherAPI

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Day=Day, Hour=Hour, Locality=Locality)


def fill_database(weater_api: 'WeatherAPI'):
    from app.models import Day, Hour, Locality
    forecast = weater_api.collect_data()
    if forecast:
        Day.query.delete()
        Hour.query.delete()
        Locality.query.delete()
        for locality, f in forecast.items():
            db.session.add(locality)
            db.session.add_all(f['daily_forecast'])
            db.session.add_all(f['hourly_forecast'])
        db.session.commit()


@app.cli.command()
def forecast():
    api_name = os.getenv('WEATHER_API') or 'TuTiempoAPI'
    if api_name == 'TuTiempoAPI':
        api = weather_factory(api_name,
                              api_key=os.getenv('WEATHER_API_KEY'),
                              locations=os.getenv('WEATHER_LOCATIONS').split(','),
                              language=os.getenv('WEATHER_LANGUAGE'))
    else:
        exit("Invalid Weather API")

    fill_database(api)
    print("Forecast updated")


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
