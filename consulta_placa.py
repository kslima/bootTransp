from selenium import webdriver
import string
import time


class ConsultaPlaca:

    @staticmethod
    def consulta_placas(placas):
        browser = webdriver.Chrome()
        consulta = {}

        for placa in placas:
            browser.get("http://infocarrosp.com.br/")
            browser.find_element_by_xpath('//*[@id="plate"]').send_keys(placa)
            browser.find_element_by_xpath('/html/body/div/div[1]/div/div[1]/form/div[2]/div/button').click()
            time.sleep(5)
            resp = browser.find_element_by_xpath('/html/body/div/div[1]/div[3]/table/tbody/tr[2]/td').text
            res = string.capwords(resp)
            res = res.split("/")
            cidade = res[0].strip()
            uf = res[1].strip()
            consulta[cidade] = uf

        return consulta


placass = ['FFX1128', 'HMV1135', 'PUB1179', 'MMX1530']
consulta = ConsultaPlaca.consulta_placas(placass)
print(consulta)