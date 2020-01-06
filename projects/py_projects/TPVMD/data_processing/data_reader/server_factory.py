import requests
import re
from utility.my_error import SettingProgramError, RequestError
from bs4 import BeautifulSoup
import abc


def read_url(url: str = ''):
    try:
        response = requests.get(url, timeout=45)
        response.raise_for_status()
    except requests.Timeout:
        raise RequestError(requests.Timeout)

    except requests.HTTPError as err:
        code = err.response.status_code
        raise RequestError("Error url: {0},  code: {1}".format(url, code))
    except requests.RequestException:
        raise RequestError("Error download url: ", url)
    else:
        return response.content


class AbstractServer(abc.ABC):
    pass


class Server(AbstractServer):
    pass


# TODO: need refactoring
class IMCESServer(Server):

    def __init__(self, server_url: str='', time_of_observation: str=''):
        self._observation_start = ''  # 01.05.2010
        self._observation_end = ''  # 01.05.2010
        self._start_url = server_url
        self._observation_start = time_of_observation[:10]
        self._observation_end = time_of_observation[10:]

    @property
    def observation_start(self):
        return self._observation_start

    @observation_start.setter
    def observation_start(self, observation_start):
        if observation_start is None or not re.match(r'\d{2}.\d{2}.\d{4}', observation_start):
            raise SettingProgramError("Incorrect data format for start observation: {}\ntry: XX.XX.XXXX".format(observation_start))
        self._observation_start = observation_start

    @property
    def observation_end(self):
        return self._observation_end

    @observation_end.setter
    def observation_end(self, observation_end):
        if observation_end is None or not re.match(r'\d{2}\.\d{2}\.\d{4}', observation_end):
            raise SettingProgramError("Incorrect data format for end observation: {}\ntry: XX.XX.XXXX".format(observation_end))
        self._observation_end = observation_end

    def check_observation(self):
        if int(self._observation_end[-4:]) <= int(self._observation_start[-4:]) \
                and int(self._observation_end[3:5]) <= int(self._observation_start[3:5]) \
                and int(self._observation_end[:2]) < int(self._observation_start[:2]):
            raise SettingProgramError("Incorrect observation interval: end {} < start {}".format(self._observation_end, self._observation_start))
        elif int(self._observation_end[-4:]) <= int(self._observation_start[-4:]) \
                and int(self._observation_end[3:5]) < int(self._observation_start[3:5]):
            raise SettingProgramError("Incorrect observation interval: end {} < start {}".format(self._observation_end, self._observation_start))
        elif int(self._observation_end[-4:]) < int(self._observation_start[-4:]):
            raise SettingProgramError("Incorrect observation interval: end {} < start {}".format(self._observation_end, self._observation_start))

    def find_file_year_url(self) -> list:
        year_url = []
        year = int(self._observation_end[-4:]) - int(self._observation_start[-4:])
        if year:
            for i in range(year+1):
                year_url.append(str(int(self._observation_start[-4:]) + i))
        else:
            year_url.append(self._observation_start[-4:])
        correct_year_url = self.check_server_year_url(year_url)
        return correct_year_url

    def check_server_year_url(self, year_url: list) -> list:
        correct_year_url = []
        content = read_url(url=self._start_url)
        soup = BeautifulSoup(content, "html5lib")
        p = soup.find_all('a')
        start_year = ''
        end_year = ''
        for href in p:
            if re.match(r'\d{4}', href.get('href')):
                start_year = href.get('href')
                break
        for href in reversed(p):
            if re.match(r'\d{4}', href.get('href')):
                end_year = href.get('href')
                break
        for year in year_url:
            if not int(start_year[:-1]) - int(year) > 0 and int(end_year[:-1]) - int(year) >= 0:
                correct_year_url.append(self._start_url + '/' + year)
            else:
                print("Not found year: {}".format(year))
        return correct_year_url

    def find_file_month_url(self, files_year_url: list) -> list:
        new_url = []
        new_url_row = []
        if len(files_year_url) == 1:
            content = read_url(url=files_year_url[0])
            soup = BeautifulSoup(content, "html5lib")
            p = soup.find_all('a')
            end_month = ()
            start_month = (5, p[5].get('href'))
            for index, href in enumerate(reversed(p)):
                if re.match(r'\d{2}_', href.get('href')):
                    end_month = (len(p)-index-1, href.get('href'))
                    break
            for index, i in enumerate(range(start_month[0], end_month[0]+1)):
                if int(self._observation_start[3:5]) <= int(p[i].get('href')[:2]) and int(self._observation_end[3:5]) >= int(p[i].get('href')[:2]):
                    new_url_row.append(files_year_url[0] + '/' + p[i].get('href'))
            new_url.append(new_url_row)
        else:
            for index, file_year_url in enumerate(files_year_url):
                new_url_row = []
                content = read_url(url=file_year_url)
                soup = BeautifulSoup(content, "html5lib")
                p = soup.find_all('a')
                end_month = ()
                start_month = (5, p[5].get('href'))
                for index2, href in enumerate(reversed(p)):
                    if re.match(r'\d{2}_', href.get('href')):
                        end_month = (len(p) - index2 - 1, href.get('href'))
                        break
                if index == 0:
                    for index2, i in enumerate(range(start_month[0], end_month[0] + 1)):
                        if int(self._observation_start[3:5]) <= int(p[i].get('href')[:2]):
                            new_url_row.append(file_year_url + '/' + p[i].get('href'))
                elif index == len(files_year_url)-1:
                    for index2, i in enumerate(range(start_month[0], end_month[0] + 1)):
                        if int(self._observation_end[3:5]) >= int(p[i].get('href')[:2]):
                            new_url_row.append(file_year_url + '/' + p[i].get('href'))
                else:
                    for index2, i in enumerate(range(start_month[0], end_month[0] + 1)):
                        new_url_row.append(file_year_url + '/' + p[i].get('href'))
                new_url.append(new_url_row)
        return new_url

    def find_file_url(self, files_month_url: list) ->list:
        new_url = []
        for year_index, file_month_url in enumerate(files_month_url):
            new_url_month = []
            for month_index, month in enumerate(file_month_url):
                new_url_day = []
                content = read_url(url=month)
                soup = BeautifulSoup(content, "html5lib")
                p = soup.find_all('a')
                end_day = ()
                start_day = (5, p[5].get('href'))
                for index2, href in enumerate(reversed(p)):
                    if re.match(r'\d{8}\.\d{2}\w', href.get('href')):
                        end_day = (len(p) - index2 - 1, href.get('href'))
                        break
                if len(files_month_url) == 1 and len(file_month_url) == 1:
                    for index2, i in enumerate(range(start_day[0], end_day[0] + 1)):
                        if int(self._observation_start[:2]) <= int(p[i].get('href')[2:4]) and int(self._observation_end[:2]) >= int(p[i].get('href')[2:4]):
                            new_url_day.append(month + p[i].get('href'))
                elif year_index == 0 and month_index == 0:
                    for index2, i in enumerate(range(start_day[0], end_day[0] + 1)):
                        if int(self._observation_start[:2]) <= int(p[i].get('href')[2:4]):
                            new_url_day.append(month + '/' + p[i].get('href'))
                elif year_index == len(files_month_url)-1 and month_index == len(file_month_url)-1:
                    for index2, i in enumerate(range(start_day[0], end_day[0] + 1)):
                        if int(self._observation_end[:2]) >= int(p[i].get('href')[2:4]):
                            new_url_day.append(month + p[i].get('href'))
                else:
                    for index2, i in enumerate(range(start_day[0], end_day[0] + 1)):
                        new_url_day.append(month + p[i].get('href'))
                new_url_month.append(new_url_day)
            new_url.append(new_url_month)
        return new_url

    def get_file_url(self) -> list:
        """
            возвращает список ссылок файлов
            :return:
        """
        self.check_observation()
        new_url = self.find_file_year_url()
        new_url = self.find_file_month_url(files_year_url=new_url)
        new_url = self.find_file_url(files_month_url=new_url)
        for year in new_url:
            for month in year:
                for day in month:
                    yield day


class ServerFactory(object):

    @staticmethod
    def create(server_type: str='', time_of_observation: str=''):
        print(server_type)
        if 'amk030.imces.ru' in server_type:
            return IMCESServer(server_type, time_of_observation)
        elif server_type == '':
            pass
        else:
            raise RuntimeError("Error")  # TODO: change raise type
