import unittest
from unittest.mock import patch
from GestionMecanica import *

class TestGestionMecanicaPositivos(unittest.TestCase):

    def setUp(self):
        # Reinicializar los datos de prueba antes de cada test
        self.usuarios_test = {
            "ADMIN": {'password': 'admin', 'perfil': 'admin', 'failed_login_count': 0},
            "TEST": {'password': 'test', 'perfil': 'mecanico', 'failed_login_count': 0},
            "BLOQUEADO": {'password': 'test', 'perfil': 'mecanico', 'failed_login_count': 3}
        }
        
        self.matriz_autos_test = [
            ['FIAT', 'PALIO', 1999, 'ABC123', 100000, 'juan perez', 'juan@mail.com'],
            ['FORD', 'FOCUS', 2015, 'XYZ789', 50000, 'maria lopez', 'maria@mail.com']
        ]

    def test_acceso_sistema_exitoso(self):
        """Prueba login exitoso"""
        with patch('builtins.input', side_effect=['ADMIN', 'admin']):
            usuario, perfil = acceso_sistema(self.usuarios_test)
            self.assertEqual(usuario, 'ADMIN')
            self.assertEqual(perfil, 'admin')
            self.assertEqual(self.usuarios_test['ADMIN']['failed_login_count'], 0)

    def test_registrar_vehiculo_exitoso(self):
        """Prueba registro exitoso de vehículo"""
        inputs = ['HONDA', 'CIVIC', '2020', 'DEF456', '30000', 'pedro gomez', 'pedro@mail.com', '-1']
        with patch('builtins.input', side_effect=inputs):
            longitud_inicial = len(self.matriz_autos_test)
            registroVehiculos(self.matriz_autos_test)
            self.assertEqual(len(self.matriz_autos_test), longitud_inicial + 1)
            nuevo_vehiculo = self.matriz_autos_test[-1]
            self.assertEqual(nuevo_vehiculo, ['HONDA', 'CIVIC', 2020, 'DEF456', 30000, 'pedro gomez', 'pedro@mail.com'])

    def test_modificar_vehiculo_exitoso(self):
        """Prueba modificación exitosa de vehículo"""
        inputs = ['ABC123', '1', 'CHEVROLET', '0'] 
        with patch('builtins.input', side_effect=inputs):
            modificar_vehiculo(self.matriz_autos_test)
            vehiculo_modificado = next(v for v in self.matriz_autos_test if v[3] == 'ABC123')
            self.assertEqual(vehiculo_modificado[0], 'CHEVROLET')

    def test_alta_usuario_exitoso(self):
        """Prueba alta exitosa de usuario"""
        with patch('builtins.input', side_effect=['NUEVO', '2']):
            longitud_inicial = len(self.usuarios_test)
            alta_usuario(self.usuarios_test)
            self.assertEqual(len(self.usuarios_test), longitud_inicial + 1)
            self.assertIn('NUEVO', self.usuarios_test)
            self.assertEqual(self.usuarios_test['NUEVO']['perfil'], 'mecanico')
            self.assertEqual(self.usuarios_test['NUEVO']['failed_login_count'], 0)

    def test_cambio_password_exitoso(self):
        """Prueba cambio exitoso de password"""
        inputs = ['1', 'newpass123', 'newpass123']
        with patch('builtins.input', side_effect=inputs):
            cambio_password(self.usuarios_test)
            self.assertEqual(self.usuarios_test['ADMIN']['password'], 'newpass123')

class TestGestionMecanicaNegativos(unittest.TestCase):

    def setUp(self):
        self.usuarios_test = {
            "ADMIN": {'password': 'admin', 'perfil': 'admin', 'failed_login_count': 0},
            "TEST": {'password': 'test', 'perfil': 'mecanico', 'failed_login_count': 0},
            "BLOQUEADO": {'password': 'test', 'perfil': 'mecanico', 'failed_login_count': 3}
        }
        
        self.matriz_autos_test = [
            ['FIAT', 'PALIO', 1999, 'ABC123', 100000, 'juan perez', 'juan@mail.com'],
            ['FORD', 'FOCUS', 2015, 'XYZ789', 50000, 'maria lopez', 'maria@mail.com']
        ]

    def test_acceso_sistema_fallido(self):
        """Prueba login fallido"""
        with patch('builtins.input', side_effect=['ADMIN', 'wrong']):
            with self.assertRaises(SystemExit):
                acceso_sistema(self.usuarios_test)
            self.assertEqual(self.usuarios_test['ADMIN']['failed_login_count'], 1)

    def test_registrar_vehiculo_datos_invalidos(self):
        """Prueba registro con datos inválidos"""
        inputs = ['HONDA', 'CIVIC', 'año_invalido', 'DEF456', '30000', 'pedro', 'mail_invalido']
        with patch('builtins.input', side_effect=inputs):
            with self.assertRaises(ValueError):
                registroVehiculos(self.matriz_autos_test)
            self.assertEqual(len(self.matriz_autos_test), 2)

    def test_modificar_vehiculo_no_existe(self):
        """Prueba modificar vehículo inexistente"""
        estado_inicial = self.matriz_autos_test.copy()
        with patch('builtins.input', side_effect=['NOEXISTE']):
            modificar_vehiculo(self.matriz_autos_test)
            self.assertEqual(self.matriz_autos_test, estado_inicial)

    def test_alta_usuario_existente(self):
        """Prueba alta de usuario que ya existe"""
        with patch('builtins.input', side_effect=['ADMIN', '1']):
            longitud_inicial = len(self.usuarios_test)
            alta_usuario(self.usuarios_test)
            self.assertEqual(len(self.usuarios_test), longitud_inicial)

    def test_cambio_password_usuario_inexistente(self):
        """Prueba cambio password para usuario que no existe"""
        inputs = ['99', 'newpass', 'newpass']
        with patch('builtins.input', side_effect=inputs):
            estado_inicial = self.usuarios_test.copy()
            cambio_password(self.usuarios_test)
            self.assertEqual(self.usuarios_test, estado_inicial)

if __name__ == '__main__':
    unittest.main()
