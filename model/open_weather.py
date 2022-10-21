class Serializable:
    @classmethod
    def from_json(cls, json_string):
        return cls(**json_string)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'


class Coord(Serializable):
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat


class Weather(Serializable):
    def __init__(self, id, main, description, icon):
        self.id = id
        self.main = main
        self.description = description
        self.icon = icon


class Main(Serializable):
    def __init__(self, temp=None, feels_like=None, temp_min=None, temp_max=None, pressure=None, sea_level=None,
                 grnd_level=None, humidity=None, temp_kf=None):
        self.temp = temp
        self.feels_like = feels_like
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.pressure = pressure
        self.sea_level = sea_level
        self.grnd_level = grnd_level
        self.humidity = humidity
        self.temp_kf = temp_kf


class Wind(Serializable):
    def __init__(self, speed, gust=None, deg=None):
        self.speed = speed
        self.gust = gust
        self.deg = deg


class Clouds(Serializable):
    def __init__(self, all):
        self.all = all


class Sys(Serializable):
    def __init__(self, type, id, country, sunrise, sunset):
        self.type = type
        self.id = id
        self.country = country
        self.sunrise = sunrise
        self.sunset = sunset


class WeatherResponse(Serializable):
    def __init__(self, coord=None, weather=None, base=None, main=None, rain=None, visibility=None, wind=None,
                 clouds=None, dt=None, sys=None, timezone=None, id=None, name=None, cod=None):
        self.coord = Coord.from_json(coord)
        self.weather = self.weather_from_list(weather)
        self.base = base
        self.rain = rain
        self.main = Main.from_json(main)
        self.visibility = visibility
        self.wind = Wind.from_json(wind)
        self.clouds = Clouds.from_json(clouds)
        self.dt = dt
        self.sys = Sys.from_json(sys)
        self.timezone = timezone
        self.id = id
        self.name = name
        self.cod = cod

    @classmethod
    def weather_from_list(cls, weathers):
        weather_list = []
        for weather in weathers:
            weather_list.append(Weather.from_json(weather))

        return weather_list


class City(Serializable):
    def __init__(self, name=None, local_names=None, lat=None, lon=None, country=None, state=None):
        self.name = name
        self.local_names = local_names
        self.lat = lat
        self.lon = lon
        self.country = country
        self.state = state
