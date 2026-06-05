{% extends 'consultas/base.html' %}

{% block content %}
<section class="card hero">
    <h2>Consulta de síntomas</h2>
    <p>Selecciona los síntomas que presenta el usuario. Al elegirlos, aparecerán a la derecha con una explicación de cómo se siente cada síntoma.</p>
</section>

{% if error %}
<div class="alert">{{ error }}</div>
{% endif %}

<section class="grid-layout">
    <form method="post" class="card form-card">
        {% csrf_token %}
        <div class="symptoms-header">
            <div>
                <h3>Síntomas disponibles</h3>
                <p class="helper-text">Marca uno o varios síntomas para analizarlos.</p>
            </div>
            <span id="selected-count" class="counter">0 seleccionados</span>
        </div>

        <div class="symptom-selector-layout">
            <div class="symptom-list-area">
                <div class="symptom-grid">
                    {% for sintoma in sintomas %}
                        <label class="symptom-item">
                            <input
                                type="checkbox"
                                name="sintomas"
                                value="{{ sintoma.valor }}"
                                data-label="{{ sintoma.texto }}"
                                data-description="{{ sintoma.descripcion }}"
                                {% if sintoma.valor in seleccionados %}checked{% endif %}
                            >
                            <span>{{ sintoma.texto }}</span>
                        </label>
                    {% endfor %}
                </div>
            </div>

            <aside class="selected-panel">
                <div class="selected-panel-header">
                    <h4>Síntomas seleccionados</h4>
                    <button type="button" id="clear-symptoms" class="clear-button">Borrar síntomas</button>
                </div>
                <div id="selected-symptoms" class="selected-symptoms">
                    <p class="empty mini">Aún no has seleccionado síntomas.</p>
                </div>
            </aside>
        </div>

        <button type="submit">Analizar síntomas</button>
    </form>

    <section class="card result-card">
        <h3>Resultado</h3>
        {% if resultado %}
            <div class="risk risk-{{ resultado.riesgo.nivel }}">
                Riesgo: {{ resultado.riesgo.nivel|title }}
            </div>

            <h4>Síntomas recibidos</h4>
            <ul>
                {% for sintoma in resultado.sintomas_recibidos %}
                    <li>{{ sintoma }}</li>
                {% endfor %}
            </ul>

            <h4>Posibles orientaciones</h4>
            {% if resultado.diagnosticos_posibles %}
                {% for item in resultado.diagnosticos_posibles %}
                    <div class="diagnosis">
                        <strong>{{ item.enfermedad }}</strong>
                        <span>{{ item.porcentaje }}% de coincidencia</span>
                        <small>Coincidencias: {{ item.coincidencias|join:", " }}</small>
                    </div>
                {% endfor %}
            {% else %}
                <p>No se encontró una coincidencia clara.</p>
            {% endif %}

            <h4>Recomendación</h4>
            <p>{{ resultado.riesgo.recomendacion }}</p>
            <p class="notice">{{ resultado.aviso }}</p>
        {% else %}
            <p class="empty">Aquí aparecerá el resultado después de enviar una consulta.</p>
        {% endif %}
    </section>
</section>

<script>
    function actualizarSintomasSeleccionados() {
        const contenedor = document.getElementById("selected-symptoms");
        const contador = document.getElementById("selected-count");
        const seleccionados = Array.from(document.querySelectorAll('input[name="sintomas"]:checked'));

        contador.textContent = seleccionados.length === 1 ? "1 seleccionado" : `${seleccionados.length} seleccionados`;
        contenedor.innerHTML = "";

        if (seleccionados.length === 0) {
            contenedor.innerHTML = '<p class="empty mini">Aún no has seleccionado síntomas.</p>';
            return;
        }

        seleccionados.forEach((input) => {
            const card = document.createElement("div");
            card.className = "selected-symptom-card";
            card.innerHTML = `
                <button type="button" class="remove-symptom" aria-label="Quitar ${input.dataset.label}">×</button>
                <strong>${input.dataset.label}</strong>
                <p>${input.dataset.description}</p>
            `;

            card.querySelector(".remove-symptom").addEventListener("click", () => {
                input.checked = false;
                actualizarSintomasSeleccionados();
            });

            contenedor.appendChild(card);
        });
    }

    document.querySelectorAll('input[name="sintomas"]').forEach((input) => {
        input.addEventListener("change", actualizarSintomasSeleccionados);
    });

    document.getElementById("clear-symptoms").addEventListener("click", () => {
        document.querySelectorAll('input[name="sintomas"]').forEach((input) => {
            input.checked = false;
        });
        actualizarSintomasSeleccionados();
    });

    actualizarSintomasSeleccionados();
</script>
{% endblock %}
