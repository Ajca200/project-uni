const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

// Configuración de almacenamiento con multer
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        const dir = './uploads';
        if (!fs.existsSync(dir)){
            fs.mkdirSync(dir);
        }
        cb(null, dir);
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + path.extname(file.originalname)); // Añadir timestamp al nombre del archivo
    }
});

const upload = multer({ storage: storage });

// Ruta para subir imágenes
app.post('/upload', upload.single('image'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('No file uploaded.');
    }
    res.send(`File uploaded: ${req.file.filename}`);
});

// Ruta para acceder a las imágenes
app.get('/image/:filename', (req, res) => {
    const filename = req.params.filename;
    const filePath = path.join(__dirname, 'uploads', filename);
    
    res.sendFile(filePath, (err) => {
        if (err) {
            res.status(404).send('Image not found');
        }
    });
});

// Servidor escuchando en el puerto definido
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
