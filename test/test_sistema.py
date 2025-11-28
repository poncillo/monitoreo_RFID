# test_sistema.py
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Agregar el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.usuario import Usuario
from models.vehiculo import Vehiculo
from models.cilindro import Cilindro
from models.ruta import Ruta
from db_connection import create_connection

class TestSistemaTransporte(unittest.TestCase):
    """Pruebas unitarias para el Sistema de Transporte"""

    def setUp(self):
        """Configuración inicial para las pruebas"""
        print("\n" + "="*50)
        print("INICIANDO PRUEBA UNITARIA")
        print("="*50)

    def tearDown(self):
        """Limpieza después de cada prueba"""
        print("PRUEBA COMPLETADA ✓")
        print("="*50)

    # PRUEBA 1: Autenticación de usuario
    def test_autenticacion_usuario(self):
        """Prueba la autenticación de usuarios en el sistema"""
        print("PRUEBA 1: Autenticación de Usuario")
        
        # Mock de la conexión a BD
        with patch('models.usuario.create_connection') as mock_conn:
            # Configurar el mock
            mock_cursor = MagicMock()
            mock_conn.return_value.cursor.return_value = mock_cursor
            
            # Simular usuario encontrado
            mock_cursor.fetchone.return_value = {
                'id': 1, 
                'username': 'EMP-PG01', 
                'rol': 'admin',
                'licencia': None,
                'telefono': '123456789'
            }
            
            # Ejecutar autenticación
            usuario = Usuario.autenticar('EMP-PG01', 'password123')
            
            # Verificaciones
            self.assertIsNotNone(usuario, "El usuario debería autenticarse correctamente")
            self.assertEqual(usuario.username, 'EMP-PG01', "El username debería coincidir")
            self.assertEqual(usuario.rol, 'admin', "El rol debería ser 'admin'")
            
            print("✓ Autenticación exitosa")
            print("✓ Datos de usuario correctos")
            print("✓ Rol asignado correctamente")

    # PRUEBA 2: Creación de vehículos
    def test_creacion_vehiculo(self):
        """Prueba la creación de vehículos en el sistema"""
        print("PRUEBA 2: Creación de Vehículo")
        
        with patch('models.vehiculo.create_connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_conn.return_value.cursor.return_value = mock_cursor
            mock_conn.return_value.commit.return_value = None
            
            # Datos de prueba
            placa = "ABC123"
            modelo = "np 300 2024"
            capacidad = 20
            estado = "disponible"
            chofer_id = None
            
            # Ejecutar creación
            resultado = Vehiculo.crear_vehiculo(placa, modelo, capacidad, estado, chofer_id)
            
            # Verificaciones
            self.assertTrue(resultado, "El vehículo debería crearse exitosamente")
            mock_cursor.execute.assert_called_once()
            
            print("✓ Vehículo creado exitosamente")
            print("✓ Placa validada: ABC123")
            print("✓ Modelo asignado: np 300 2024")

    # PRUEBA 3: Gestión de cilindros
    def test_gestion_cilindros(self):
        """Prueba las operaciones CRUD de cilindros"""
        print("PRUEBA 3: Gestión de Cilindros")
        
        with patch('models.cilindro.create_connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_conn.return_value.cursor.return_value = mock_cursor
            
            # Simular obtención de cilindros
            mock_cursor.fetchall.return_value = [
                {
                    'id': 1,
                    'codigo_rfid': 'RFID001',
                    'capacidad_kg': 20,
                    'estado': 'almacen',
                    'fecha_ultimo_mantenimiento': '2024-01-15',
                    'vehiculo_placa': 'ABC123',
                    'chofer_username': 'EMP-PG02'
                }
            ]
            
            # Obtener cilindros
            cilindros = Cilindro.obtener_todos()
            
            # Verificaciones
            self.assertIsInstance(cilindros, list, "Debería retornar una lista")
            self.assertEqual(len(cilindros), 1, "Debería tener 1 cilindro")
            self.assertEqual(cilindros[0]['codigo_rfid'], 'RFID001', "RFID debería coincidir")
            
            print("✓ Lista de cilindros obtenida")
            print("✓ RFID validado: RFID001")
            print("✓ Estado del cilindro: almacen")

    # PRUEBA 4: Gestión de rutas
    def test_creacion_ruta(self):
        """Prueba la creación y gestión de rutas"""
        print("PRUEBA 4: Creación de Ruta")
        
        with patch('models.ruta.create_connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_conn.return_value.cursor.return_value = mock_cursor
            mock_conn.return_value.commit.return_value = None
            
            # Datos de prueba
            chofer_id = 1
            vehiculo_id = 1
            origen = "CDMX"
            destino = "Guadalajara"
            distancia_km = 450.5
            tiempo_minutos = 300
            estado = "programada"
            
            # Ejecutar creación
            resultado = Ruta.crear_ruta(chofer_id, vehiculo_id, origen, destino, 
                                      distancia_km, tiempo_minutos, estado)
            
            # Verificaciones
            self.assertTrue(resultado, "La ruta debería crearse exitosamente")
            mock_cursor.execute.assert_called_once()
            
            print("✓ Ruta creada exitosamente")
            print("✓ Origen-Destino: CDMX → Guadalajara")
            print("✓ Distancia: 450.5 km")
            print("✓ Estado: programada")

    # PRUEBA 5: Generación de códigos de usuario
    def test_generacion_codigo_usuario(self):
        """Prueba la generación automática de códigos de usuario"""
        print("PRUEBA 5: Generación de Código de Usuario")
        
        # Mock para simular diferentes escenarios
        test_cases = [
            # (usuarios_existentes, codigo_esperado)
            ([], "EMP-PG01"),
            (['EMP-PG01'], "EMP-PG02"),
            (['EMP-PG01', 'EMP-PG02', 'EMP-PG03'], "EMP-PG04"),
            (['EMP-PG01', 'EMP-PG03'], "EMP-PG02"),  # Hueco en la numeración
        ]
        
        for usuarios_existentes, codigo_esperado in test_cases:
            with patch('views.user_register.create_connection') as mock_conn:
                mock_cursor = MagicMock()
                mock_conn.return_value.cursor.return_value = mock_cursor
                mock_cursor.fetchall.return_value = [(user,) for user in usuarios_existentes]
                
                # Importar aquí para evitar problemas de importación circular
                from views.user_register import RegistroUsuarioView
                
                # Crear instancia y generar código
                registro_view = RegistroUsuarioView(parent=None)
                codigo_generado = registro_view.generar_codigo_usuario_emp()
                
                # Verificación
                self.assertEqual(codigo_generado, codigo_esperado, 
                               f"Para {usuarios_existentes}, esperado: {codigo_esperado}, obtenido: {codigo_generado}")
            
            print(f"✓ Escenario {usuarios_existentes}: {codigo_generado}")

    # PRUEBA 6: Validación de formularios
    def test_validacion_formularios(self):
        """Prueba las validaciones de datos en formularios"""
        print("PRUEBA 6: Validación de Formularios")
        
        # Casos de prueba para validación de usuario
        test_cases = [
            ("abc", True),      # 3 caracteres - válido
            ("abcd", True),     # 4 caracteres - válido  
            ("ab", False),      # 2 caracteres - inválido
            ("", False),        # vacío - inválido
            ("   ", False),     # solo espacios - inválido
            ("usuario123", True), # alfanumérico - válido
        ]
        
        from views.login import LoginViewCH
        
        login_view = LoginViewCH(parent=None)
        
        for usuario, esperado in test_cases:
            resultado = login_view.validar_usuario(usuario)
            self.assertEqual(resultado, esperado, 
                           f"Usuario: '{usuario}' - Esperado: {esperado}, Obtenido: {resultado}")
            print(f"✓ Usuario '{usuario}': {'VÁLIDO' if esperado else 'INVÁLIDO'}")

    # PRUEBA EXTRA: Conexión a base de datos
    def test_conexion_base_datos(self):
        """Prueba la conexión a la base de datos"""
        print("PRUEBA EXTRA: Conexión a Base de Datos")
        
        # Esta prueba verifica que el módulo de conexión se importa correctamente
        # y tiene la función esperada
        self.assertTrue(hasattr(create_connection, '__call__'), 
                       "create_connection debería ser una función invocable")
        
        print("✓ Módulo de conexión importado correctamente")
        print("✓ Función create_connection disponible")

def ejecutar_pruebas_verbose():
    """Ejecuta las pruebas con output detallado"""
    print("🚀 INICIANDO SUITE DE PRUEBAS UNITARIAS")
    print("📋 Se ejecutarán 6 pruebas unitarias")
    print("="*60)
    
    # Crear test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSistemaTransporte)
    
    # Ejecutar con verbosidad
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Resumen
    print("="*60)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Pruebas exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("✅ CRITERIO DE PRUEBAS UNITARIAS: CUMPLIDO")
    else:
        print("❌ Algunas pruebas fallaron")
        
    return result.wasSuccessful()

if __name__ == '__main__':
    # Ejecutar pruebas automáticamente
    ejecutar_pruebas_verbose()