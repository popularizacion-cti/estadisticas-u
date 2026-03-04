let globalData = null;

fetch("data.json")
.then(response => response.json())
.then(data => {
    globalData = data;

    const nivelSelect = document.getElementById("nivel");
    const niveles = Object.keys(data["Tradicional"]);

    niveles.forEach(nivel => {
        const option = document.createElement("option");
        option.value = nivel;
        option.textContent = nivel;
        nivelSelect.appendChild(option);
    });

    renderizarGrafica();

    nivelSelect.addEventListener("change", renderizarGrafica);
    document.querySelectorAll("input[name='clasificacion']")
        .forEach(r => r.addEventListener("change", renderizarGrafica));
});

function renderizarGrafica() {

    const nivel = document.getElementById("nivel").value;
    const clasificacion = document.querySelector("input[name='clasificacion']:checked").value;

    const datos = globalData[clasificacion][nivel]["Nacional"];

    const sectores = [...new Set(datos.map(d => d.Sector))];

    const traces = sectores.map(sector => {
        const datosSector = datos.filter(d => d.Sector === sector);

        return {
            x: datosSector.map(d => d.Fecha_postulacion),
            y: datosSector.map(d => d.Porcentaje),
            mode: "lines+markers",
            name: sector
        };
    });

    Plotly.newPlot("grafica", traces, {
        xaxis: { title: "Año de postulación" },
        yaxis: { title: "Porcentaje (%)" }
    });
}