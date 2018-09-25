import numpy as np
import math

saturated_water_vapor_pressure = {-20: 0.1, 0:0.61129, 1:0.65716,} # Давление насыщенного пара воды http://www.fptl.ru/spravo4nik/davlenie-vodyanogo-para.html
                                                                   # http://school-physics.spb.ru/data/labs/Saturated_steam.pdf
partial_saturated_water_vapor_pressure ={0:611}  # Парциональное Давление насыщенного пара воды # http://minkor.ru/upload/spravochnik/101009-8.pdf


class MeteorologicalMath(object):

    def mean(self, x, col: int=0) -> np.ndarray:
        return np.mean(x[:, col], axis=0)

    def var(self, x, col: int=0) -> np.ndarray:
        return np.var(x[:, col], axis=0)

    def std(self, x, col: int=0) -> np.ndarray:
        return np.std(x[:, col], axis=0)

    def modulus_of_the_mean_vector(self, list_x: list=None):
        return math.sqrt(sum(list(map(lambda x: pow(x, 2), list_x))))

    def angle_of_inclination_to_the_horizon_of_the_mean_vector(self, v_mean_horizontal, v_mean):
        return math.acos(v_mean_horizontal/v_mean)

    def horizontal_wind_speed_direction(self, vs, ve):
        f = math.atan((-ve)/vs)
        if vs > 0.01:
            return math.pi*f
        elif vs < -0.01 and ve >=0:
            return f
        elif vs < -0.01 and ve < 0:
            return 2*math.pi+f
        elif math.fabs(vs) <= 0.01 and ve >=0:
            return math.pi/2
        else:
            return 3*math.pi/2

    def elasticity_of_water_vapor(self, r, t):
        return r*saturated_water_vapor_pressure[t]/100

    def moisture_deficit(self, e, t):
        return saturated_water_vapor_pressure[t]-e

    def absolute_humidity(self, e, t):
        alpha = 1./273
        return (0.81*e)/(1+alpha*t)

    def dwe_point(self, r, t):
        r /= 100
        b_ros = 237.7
        a_ros = 17.27
        return (b_ros*((a_ros*t)/(b_ros+t)+math.log(r)))/(a_ros-((a_ros*t)/(b_ros+t)))

    def concentration_of_moisture(self, r, t):
        return 216.679*r*partial_saturated_water_vapor_pressure[int(t)]/(10000*(t+273.16))

    def air_density(self, p, r, t):
        # TODO: перевисти t в Кельвины
        return (0.003483/t)*(p-0.3779*r*saturated_water_vapor_pressure[int(t)])

    def speed_of_sound_in_air(self, t):
        return 331.4+0.6*t

    def calculate_all_param(self, data):
        """
        data row:
        0 - time
        1 - T(Температура воздуха), C
        2 - vx(Южный компонент) м/с
        3 - vy(Восточный компонент) м/с
        4 - w(Вертикальный компонент) м/с
        5 - P(Атмосферное давление) мм.рт.ст
        6 - r(Относительная влажность воздуха) %
        7 - error(Признак ошибки)
        """
        ##########################################################################

                                #  Характеристики воздуха

        t_sr = self.mean(data, 1)  # Средняя теспература воздуха, C
        t_sigma = self.std(data, 1)  # Стандартное отклонение теспературы, C
        p_sr = self.mean(data, 5)  # Среднее значение атмосферного давления, мм.рт.ст
        r_sr = self.mean(data, 6)  # среднее значение относительной влажности воздуха, %
        e = self.elasticity_of_water_vapor(r_sr, int(t_sr))  # Упругость(давление) водяного пара, гПА
        e_d = self.moisture_deficit(e, int(t_sr))  # Дефицит влажности, гПА
        t_d = self.dwe_point(r_sr, t_sr)  # Температура точки росы, С
        q = self.absolute_humidity(e, t_sr)  # Абсолюная влажность воздуха, г/м
        m = self.concentration_of_moisture(r_sr, t_sr)  # массовая концентрация влаги, о/оо
        p = self.air_density(p_sr, r_sr, t_sr)  # плотность воздуха, г/м
        c = self.speed_of_sound_in_air(t_sr)  # скорость звука в воздухе, м/с
        #######################################################################

                                #  Характеристики ветра

        v_sr = self.modulus_of_the_mean_vector([self.mean(data, 2), self.mean(data, 3)])  # средняя скорость горизонтального ветра, м/с
        v_min = None  #
        v_max = None  #
        v_sigma = self.modulus_of_the_mean_vector([self.std(data, 2), self.std(data, 3)])  # стандартное отклонение скорости горизонтального вектора, м/с | неправильно переделать!
        d_sr = self.horizontal_wind_speed_direction(vs=self.mean(data, 2), ve=self.mean(data, 3)) # среднее направление горизонтального ветра, TODO: чекнуть возвращаемое значение
        d_sr_sigma = None  #
        w_sr = self.mean(data, 4)  # средняя скорость вертикального ветра, м/с
        w_sigma = self.std(data, 4)  # стандартное отклонение скорости вертикального ветра, м/с
        w_abc = self.modulus_of_the_mean_vector([self.mean(data, 2), self.mean(data, 3), self.mean(data, 4)])  # модуль среднего вектора скорости ветра, м/с
        alpha = self.angle_of_inclination_to_the_horizon_of_the_mean_vector(v_sr, w_abc)  # угол наклона к горизонту среднего вектора скорости ветра, TODO чекнуть возр знач
        v_s = self.mean(data, 2)  # среднее значение южного компонента скорости ветра, м/с
        v_v = self.mean(data, 3)  # среднее значение восточного компонента скорости ветра, м/с
