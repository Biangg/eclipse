document.addEventListener('DOMContentLoaded', function () {
    // Selecciona todos los enlaces principales del menú
    const navLinks = document.querySelectorAll('.nav-list > li > a');
    const subLists = document.querySelectorAll('.sub-list');
    const contentBlock = document.querySelector('main');

    // Función para desactivar todos los enlaces y ocultar sublistas
    function resetNav() {
        navLinks.forEach(link => link.classList.remove('active'));
        subLists.forEach(list => list.style.display = 'none');
    }

    // Función para activar un enlace y mostrar su sub-list
    function activateNav(link) {
        resetNav();
        link.classList.add('active');
        // Mostrar la sub-list siguiente al enlace si existe
        // const nextUl = link.parentElement.nextElementSibling;
        // if (nextUl && nextUl.classList.contains('sub-list')) {
        //     nextUl.style.display = 'block';
        // }
    }

    // Función para cargar la interfaz de cada sección en el block content
    function loadSection(section) {
        let html = '';
        switch (section) {
            case 'GeneralConfig':
                html = `
                    <div id="Ajustes" class="section_main">
                        <div class="section_header">
                            <h2>Ajustes Generales</h2>

                            <label for="toggle">Activar copia de seguridad</label>
                            <input type="checkbox" name="toggle" id="CopiaSeguridad">

                            <p class="nota">Configura los ajustes generales de tu tienda, como el nombre, correo electrónico y opciones de copia de seguridad.</p>
                        </div>

                        <form action="#" method="post" class="ajustes_form" enctype="multipart/form-data">
                            <div class="form_group">
                                <label for="logo">Logotipo de la tienda</label>
                                <input type="file" id="logo" name="logo" accept="image/*">
                            </div>
                            <div class="form_group">
                                <label for="nombre">Nombre de la tienda</label>
                                <input type="text" id="nombre" name="nombre" placeholder="Nombre de la tienda">
                            </div>
                            <div class="form_group">
                                <label for="idioma">Idioma</label>
                                <select id="idioma" name="idioma">
                                    <option value="es">Español</option>
                                    <option value="en">Inglés</option>
                                    <option value="fr">Francés</option>
                                </select>
                            </div>
                            <div class="form_group">
                                <label for="moneda">Moneda</label>
                                <select id="moneda" name="moneda">
                                    <option value="mxn">Peso Mexicano (MXN)</option>
                                    <option value="usd">Dólar Estadounidense (USD)</option>
                                    <option value="eur">Euro (EUR)</option>
                                </select>
                            </div>
                            <div class="form_group">
                                <label for="direccion">Dirección</label>
                                <input type="text" id="direccion" name="direccion" placeholder="Dirección de la tienda">
                            </div>
                            <div class="form_group">
                                <label for="pais">País</label>
                                <input type="text" id="pais" name="pais" placeholder="País">
                            </div>
                            <div class="form_group">
                                <label for="ciudad">Ciudad</label>
                                <input type="text" id="ciudad" name="ciudad" placeholder="Ciudad">
                            </div>
                            <button type="submit" class="btn_guardar">Guardar cambios</button>
                        </form>
                    </div>
                `;
                break;
            case 'UsuariosPermisos':
                html = `<div id="Usuarios" class="section_main">
                            <div class="section_header usuarios_header">
                                <h2>Usuarios y Permisos</h2>
                                <p class="nota">
                                    Gestión de usuarios y roles.
                                </p>
                            </div>

                            <div class="usuarios_container">
                                <div class="usuario_form_group">
                                    <input type="text" id="nombre_usuario" placeholder="Nombre de usuario">
                                    <input type="email" id="email_usuario" placeholder="Correo electrónico">
                                    <input type="password" id="password_usuario" placeholder="Contraseña">
                                    <select id="rol_usuario">
                                        <option value="">Selecciona un rol</option>
                                        <option value="admin">Administrador</option>
                                        <option value="editor">Editor</option>
                                        <option value="viewer">Visualizador</option>
                                    </select>
                                    <button class="btn_guardar" id="btn_agregar_usuario">Agregar usuario</button>
                                </div>

                                <table class="usuarios_tabla">
                                    <thead>
                                        <tr>
                                            <th>Usuario</th>
                                            <th>Email</th>
                                            <th>Rol</th>
                                            <th>Acciones</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <!-- Ejemplo de usuario, reemplazar por datos dinámicos -->
                                        <tr>
                                            <td>Juan Pérez</td>
                                            <td>juan@email.com</td>
                                            <td>Administrador</td>
                                            <td>
                                                <button class="btn_editar">Editar</button>
                                                <button class="btn_eliminar">Eliminar</button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>Ana López</td>
                                            <td>ana@email.com</td>
                                            <td>Editor</td>
                                            <td>
                                                <button class="btn_editar">Editar</button>
                                                <button class="btn_eliminar">Eliminar</button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                `;
                break;
            case 'Inventario':
                html = `<div id="Inventario" class="section_main">
    <div class="section_header inventario_header">
        <h2>Inventario</h2>
        <p class="nota">
            Configura el control de stock, alertas y categorías de productos.
        </p>
    </div>

    <div class="inventario_container">
        <div class="inventario_opciones">
            <div class="inventario_switch">
                <label for="control_stock">Activar control de stock</label>
                <input type="checkbox" id="control_stock">
            </div>
            <div class="inventario_switch">
                <label for="alerta_stock">Activar alertas por bajo stock</label>
                <input type="checkbox" id="alerta_stock">
            </div>
        </div>

        <div class="inventario_categorias">
            <h3>Categorías de producto</h3>
            <div class="categorias_form">
                <input type="text" id="nueva_categoria" placeholder="Nueva categoría">
                <button class="btn_guardar" id="btn_agregar_categoria">Agregar</button>
            </div>
            <ul class="categorias_lista">
                <li>Electrónica <button class="btn_eliminar_categoria">Eliminar</button></li>
                <li>Ropa <button class="btn_eliminar_categoria">Eliminar</button></li>
                <li>Alimentos <button class="btn_eliminar_categoria">Eliminar</button></li>
            </ul>
        </div>

        <div class="inventario_unidades">
            <h3>Unidad predeterminada</h3>
            <select id="unidad_predeterminada">
                <option value="pieza">Pieza</option>
                <option value="kg">Kilogramo</option>
                <option value="lt">Litro</option>
                <option value="m">Metro</option>
            </select>
        </div>
    </div>
</div>`;
                break;
            case 'IA':
                html = `<div id="Recomendaciones" class="section_main">
    <div class="section_header recomendaciones_header">
        <h2>IA y Recomendaciones</h2>
        <p class="nota">
            Predicciones de venta, sugerencias de reposición y recomendaciones de precios en francos CFA (BEAC).
        </p>
    </div>

    <div class="recomendaciones_cards_container">
        <div class="recomendacion_card">
            <h3>Predicción de Ventas</h3>
            <p class="recomendacion_valor">+12% esta semana</p>
            <p class="recomendacion_desc">Se espera un aumento en las ventas de bebidas energéticas. Considera aumentar el stock.</p>
        </div>
        <div class="recomendacion_card">
            <h3>Reposición Sugerida</h3>
            <p class="recomendacion_valor">Vodka: 15 botellas</p>
            <p class="recomendacion_desc">El inventario de vodka está por debajo del mínimo recomendado. Sugerimos reponer pronto.</p>
        </div>
        <div class="recomendacion_card">
            <h3>Recomendación de Precios (BEAC)</h3>
            <p class="recomendacion_valor">Gin Tonic: 2,500 FCFA</p>
            <p class="recomendacion_desc">Ajusta el precio del Gin Tonic para maximizar el margen según la demanda actual.</p>
        </div>
    </div>
</div>`;
                break;
            case 'Integraciones':
                html = `<div id="Integraciones" class="section_main">
    <div class="section_header integraciones_header">
        <h2>Integraciones</h2>
        <p class="nota">
            Importa y exporta datos, realiza copias de seguridad y genera reportes de tu tienda.
        </p>
    </div>

    <div class="integraciones_container">
        <div class="integracion_group">
            <h3>Importar archivos</h3>
            <form class="importar_form form_cont">
                <input type="file" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel">
                <button class="btn_guardar" type="submit">Importar</button>
            </form>
        </div>
        <div class="integracion_group">
            <h3>Exportar archivos</h3>
            <button class="btn_guardar">Exportar CSV</button>
            <button class="btn_guardar">Exportar Excel</button>
        </div>
        <div class="integracion_group">
            <h3>Copia de seguridad</h3>
            <button class="btn_guardar">Generar copia de seguridad</button>
            <button class="btn_guardar">Restaurar copia</button>
        </div>
        <div class="integracion_group">
            <h3>Reportes</h3>
            <button class="btn_guardar">Generar reporte de ventas</button>
            <button class="btn_guardar">Generar reporte de inventario</button>
        </div>
    </div>
</div>`;
                break;
            // Por si creo una nueva sección sin un ID (Lo Boraré cuando complete todas)
            default:
                html = `<div class="section_main"><h2>Bienvenido</h2></div>`;
        }
        contentBlock.innerHTML = html;
    }

    // Asigna eventos a los enlaces principales
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            activateNav(this);

            // Determina la sección a mostrar según el id o texto
            let section = this.id || this.textContent.replace(/\s/g, '');
            loadSection(section);
        });
    });

    // Estado inicial: GeneralConfig activo y su sub-list visible (si existe)
    const generalLink = document.getElementById('GeneralConfig');
    if (generalLink) {
        activateNav(generalLink);
        loadSection('GeneralConfig');
    }
});