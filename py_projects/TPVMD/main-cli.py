from data_processing.data_reader.reader import Reader
import click
from utility.my_error import SettingProgramError, RequestError
import configparser
from data_processing.tpvmd_math.meteorological_math import MeteorologicalMath


def read_func(url: str='', observation_start: str='', observation_end: str=''):
    try:
        reader = Reader()
        reader.set_read_from(read_from='local')
        # data = reader.read_file(path_or_server=url, time_of_observation=observation_start + observation_end)
        data = reader.read_file(path_or_server='09010003.07B')
        m = MeteorologicalMath()
        # print(m.mean(data))
        # print(m.var(data))
        # print(m.std(data))
        # print(m.modulus_of_the_mean_vector([m.mean(data, 0), m.mean(data, 1)]))
        # m.calculate_all_param(data)
    except SettingProgramError as e:
        print("SettingProgramError: {}".format(e))
    except RequestError as e:
        print("RequestError: {}".format(e))


@click.command()
@click.option('--url', default='http://amk030.imces.ru/meteodata/AMK_030_BIN/', type=str, help='url.')
@click.option('--observation_start', default='08.07.2008', type=str, help='Observation start.')
@click.option('--observation_end', default='08.07.2008', type=str, help='Observation end.')
@click.option('--smoothing_interval', default=12.5, type=float, help='Smoothing interval.')
@click.option('--observation_interval', default='', help='Observation interval.')
@click.option('--t/--no-t', default=True, help='Air temperature.')
@click.option('--vx/--no-vx', default=True, help='Southern component of wind speed.')
@click.option('--vy/--no-vy', default=True, help='Eastern component of wind speed.')
@click.option('--w/--no-w', default=True, help='Vertical component of wind speed.')
@click.option('--p/--no-p', default=True, help='Atmosphere pressure.')
@click.option('--r/--no-r', default=True, help='Relative air humidity.')
@click.option('--config_file', default=None, help='config_file.')
def main(url, observation_start, observation_end, smoothing_interval, observation_interval, t, vx, vy, w, p, r, config_file):
    if config_file:
        config_file_ = configparser.ConfigParser()
        config_file_.read(config_file)
        url = config_file_['program_setting']['url']
        observation_start = config_file_['program_setting']['observation_start']
        observation_end = config_file_['program_setting']['observation_end']
        read_func(url=url, observation_start=observation_start, observation_end=observation_end)
    else:
        read_func(url=url, observation_start=observation_start, observation_end=observation_end)


if __name__ == '__main__':
    main()
