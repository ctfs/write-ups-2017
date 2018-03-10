const express = require('express');
const app = express();

app.use(express.static('public'));
app.set('view engine', 'ejs');

//port to run server
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
    res.render('index');
});

app.listen(PORT, () => {
    console.log(`It's on ${PORT} man`);
});