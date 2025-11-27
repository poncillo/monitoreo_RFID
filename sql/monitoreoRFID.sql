-- DIPSY --
-- Tabla 1: Usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'general', 'chofer') NOT NULL,
    telefono VARCHAR(20),
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Tabla 2: Choferes--
CREATE TABLE choferes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'general', 'chofer') NOT NULL,
    licencia VARCHAR(50) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla 3: Vehículos
CREATE TABLE vehiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    modelo VARCHAR(100),
    capacidad_cilindros INT NOT NULL,
    estado ENUM('disponible', 'mantenimiento', 'ocupado') DEFAULT 'disponible',
    chofer_asignado traer el de id_choferes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla 4: Rutas
CREATE TABLE rutas (
    id_ruta INT AUTO_INCREMENT PRIMARY KEY,
    id_chofer INT NOT NULL,
    id_vehiculo INT NOT NULL,
    origen VARCHAR(255) NOT NULL,
    destino VARCHAR(255) NOT NULL,
    distancia_km DECIMAL(8,2),
    tiempo_estimado_min INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    FOREIGN KEY (id_chofer) REFERENCES choferes(id_usuario),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo)
);

-- Tabla 5: Cilidnros--
CREATE TABLE cilindros (
    id_cilindro INT AUTO_INCREMENT PRIMARY KEY,
    codigo_rfid VARCHAR(64) UNIQUE NOT NULL, -- Identificador único del chip RFID
    capacidad_kg DECIMAL(5,2) NOT NULL,
    estado ENUM('almacen', 'en_ruta', 'entregado', 'mantenimiento') DEFAULT 'almacen',
    fecha_ultimo_mantenimiento DATE,
    id_vehiculo_actual INT NULL, -- Cilindro cargado en un vehículo
    FOREIGN KEY (id_vehiculo_actual) REFERENCES vehiculos(id_vehiculo)
);

-- DIPSY --