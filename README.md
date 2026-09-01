# QA Project: Urban Routes

## Descripción del proyecto

Suite de pruebas automatizadas end-to-end para **Urban Routes**, una aplicación web de pedido de taxis. Las pruebas cubren el flujo completo de un pedido:

1. Configurar la dirección de origen y destino.
2. Seleccionar la tarifa **Comfort**.
3. Rellenar y confirmar el número de teléfono (incluyendo el código SMS).
4. Agregar una tarjeta de crédito.
5. Escribir un mensaje para el conductor.
6. Pedir manta y pañuelos.
7. Pedir 2 helados.
8. Confirmar el pedido y comprobar que aparece el modal de búsqueda de taxi.
9. Esperar a que se asigne un conductor y se muestre su información (paso opcional).

## Tecnologías y técnicas utilizadas

- **Python 3**
- **Selenium WebDriver** para la automatización del navegador
- **pytest** como framework de pruebas
- **Page Object Model (POM)**: los localizadores y las acciones sobre la página viven en la clase `UrbanRoutesPage`, y los casos de prueba en `TestUrbanRoutes`, ambas en [main.py](main.py)
- **Chrome DevTools Protocol (performance log)** para interceptar la petición de red que contiene el código de confirmación del teléfono (función `retrieve_phone_code`)
- Esperas explícitas (`WebDriverWait` / `expected_conditions`) en lugar de `sleep()`, para sincronizar las pruebas con el estado real de la interfaz

## Estructura del proyecto

```
qa-project-Urban-Routes-es/
├── data.py     # URL del servidor y datos de prueba (dirección, teléfono, tarjeta, mensaje)
├── main.py     # UrbanRoutesPage (localizadores y métodos) y TestUrbanRoutes (casos de prueba)
└── README.md
```

## Cómo ejecutar las pruebas

1. Instala las dependencias:
   ```
   pip install selenium pytest
   ```
2. Genera una URL de servidor desde la plataforma de TripleTen y cópiala completa (incluyendo `?lng=es`) en la variable `urban_routes_url` de [data.py](data.py).
3. Ejecuta las pruebas desde la raíz del proyecto:
   ```
   pytest main.py -v
   ```

Las pruebas abren Google Chrome automáticamente (se requiere tenerlo instalado); Selenium gestiona el driver correspondiente.
