-- DIPSY --
-- Tabla 1: Usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'general', 'chofer') NOT NULL,
    licencia VARCHAR(50) UNIQUE DEFAULT NULL,
    telefono VARCHAR(20),
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla 2: Vehículos
CREATE TABLE vehiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    modelo VARCHAR(100),
    capacidad_cilindros INT NOT NULL,
    estado ENUM('disponible', 'mantenimiento', 'ocupado') DEFAULT 'disponible',
    chofer_id INT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    FOREIGN KEY (chofer_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Tabla 3: Rutas
CREATE TABLE rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chofer_id INT NOT NULL,
    vehiculo_id INT NOT NULL,
    origen VARCHAR(255) NOT NULL,
    destino VARCHAR(255) NOT NULL,
    distancia_km DECIMAL(8,2),
    tiempo_estimado_min INT,
    estado ENUM('programada', 'en_camino', 'completada', 'cancelada') DEFAULT 'programada',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chofer_id) REFERENCES users(id),
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id)
);

-- Tabla 4: Cilidnros--
CREATE TABLE cilindros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_rfid VARCHAR(64) UNIQUE NOT NULL,
    capacidad_kg DECIMAL(5,2) NOT NULL CHECK (capacidad_kg > 0),
    estado ENUM('almacen', 'en_ruta', 'entregado', 'mantenimiento') DEFAULT 'almacen',
    fecha_ultimo_mantenimiento DATE,
    vehiculo_id INT NULL,
    ruta_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id) ON DELETE SET NULL,
    FOREIGN KEY (ruta_id) REFERENCES rutas(id) ON DELETE SET NULL
);

-- Tabla 5: Historial de Ubicaciones (Para trazabilidad y mapas)
CREATE TABLE historial_ubicaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehiculo_id INT NOT NULL,
    latitud DECIMAL(10, 8) NOT NULL,
    longitud DECIMAL(11, 8) NOT NULL,
    fecha_reporte DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id)
);

-- DIPSY --

-- Creación de usuario manual para prueba --
USE monitoreo_rfid_db;

INSERT INTO users (username, password_hash, rol, licencia, telefono) 
VALUES ('admin', '1234', 'admin', 'LIC-001', '555-0001');