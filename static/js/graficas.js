//Inicializar elementos
const el_KY_001 = document.getElementById('el_KY_001');
const el_KY_021 = document.getElementById('el_KY_021');
const el_KY_032 = document.getElementById('el_KY_032');
//Contadores
let cuenta = 1;
//Data
let data_KY_001 = {
    labels: [],
    datasets: [{
        label: "Sensor de temperatura KY 001",
        data: [],
        borderWidth: 1
    }]
}
let data_KY_021 = {
    labels: [],
    datasets: [{
        label: "Sensor magnetico KY 021",
        data: [],
        borderWidth: 1,
        stepped: true
    }]
}
let data_KY_032 = {
    labels: [],
    datasets: [{
        label: "Sensor de proximidad KY 032",
        data: [],
        borderWidth: 1,
        stepped: true
    }]
}

//Inicializar graficas
let chart_KY_001 = new Chart(el_KY_001, {
    type: 'line',
    data: data_KY_001,
    options: {
        scales: {
            y: {
                offset: true,
                position: 'left'
            }
        }
    }
});
let chart_KY_021 = new Chart(el_KY_021, {
    type: 'line',
    data: data_KY_021,
    options: {
        scales: {
            y: {
                type: 'category',
                labels: ['ON', 'OFF'],
                offset: true,
                position: 'left',
                stack: 'demo',
                stackWeight: 1,
                border: {
                    color: "#000"
                }
            }
        }
    }
});
let chart_KY_032 = new Chart(el_KY_032, {
    type: 'line',
    data: data_KY_032,
    options: {
        scales: {
            y: {
                type: 'category',
                labels: ['ON', 'OFF'],
                offset: true,
                position: 'left',
                stack: 'demo',
                stackWeight: 1,
                border: {
                    color: "#000"
                }
            }
        }
    }
});

chart_KY_032.canvas.style.height = '100%';

let intervalo;





document.querySelector("#i_inter").addEventListener("click", (e) => {
    if (typeof intervalo == 'undefined') {
        intervalo = setInterval(() => {
            fetch('/obtener-data')
                .then((response) => response.json())
                .then((json) => {

                    chart_KY_001.data.labels.push(cuenta);
                    chart_KY_021.data.labels.push(cuenta);
                    chart_KY_032.data.labels.push(cuenta);

                    chart_KY_001.data.datasets.forEach((dataset) => {
                        dataset.data.push(json.KY_001.C);
                    });
                    chart_KY_021.data.datasets.forEach((dataset) => {
                        dataset.data.push(json.KY_021);
                    });
                    chart_KY_032.data.datasets.forEach((dataset) => {
                        dataset.data.push(json.KY_032);
                    });
                    cuenta++;
                    chart_KY_001.update();
                    chart_KY_021.update();
                    chart_KY_032.update();

                    console.log(json);
                })
                .catch((error) => {
                    console.log(error);
                });
        }, 1000)
    }
    else{
        console.log(typeof intervalo );
    }
})

document.querySelector("#d_inter").addEventListener("click", (e) => {
    clearInterval(intervalo)
    intervalo = undefined
})

document.querySelector("#borrar").addEventListener("click", (e) => {

    chart_KY_001.data.labels = [];
    chart_KY_001.data.datasets.forEach((dataset) => {
        dataset.data = []
    });
    chart_KY_021.data.labels = [];
    chart_KY_021.data.datasets.forEach((dataset) => {
        dataset.data = []
    });
    chart_KY_032.data.labels = [];
    chart_KY_032.data.datasets.forEach((dataset) => {
        dataset.data = []
    });
    chart_KY_001.update();
    chart_KY_021.update();
    chart_KY_032.update();

})


