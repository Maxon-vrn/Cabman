ymaps.ready(init);

function init() {
    // Стоимость за километр.
    var DELIVERY_TARIFF = 16,
    // Минимальная стоимость.
        MINIMUM_COST = 400,
        myMap = new ymaps.Map('map', {
            center: [51.66114505, 39.20129184],//координат центра карты
            zoom: 11, // увеличение карты от 0-19 чем больше тем крупнее объекты
            controls: [],   //елементы управления. если пустой- убрали все элементы управления
            behaviors: ['drag'] //отключение увеличения колесиком и перетаскивание левой кнопкой мыши
        }),
        
    // Создадим панель маршрутизации.
        routePanelControl = new ymaps.control.RoutePanel({
            options: {
                // Добавим заголовок панели.
                showHeader: true,
                title: 'Расчёт стоимости поездки'
            }
        }),
        zoomControl = new ymaps.control.ZoomControl({
            options: {
                size: 'medium',
                float: 'none',
                position: {
                    bottom: 150,
                    right: 20
                }
            }
        });
    // Пользователь сможет построить только автомобильный маршрут.
    routePanelControl.routePanel.options.set({
        types: {auto: true}
    });

    // Если вы хотите задать неизменяемую точку "откуда", раскомментируйте код ниже.
    /*routePanelControl.routePanel.state.set({
        fromEnabled: false,
        from: 'Москва, Льва Толстого 16'
     });*/

    myMap.controls.add(routePanelControl).add(zoomControl);

    // Получим ссылку на маршрут.
    routePanelControl.routePanel.getRouteAsync().then(function (route) {

        // Зададим максимально допустимое число маршрутов, возвращаемых мультимаршрутизатором.
        route.model.setParams({results: 1}, true);

        // Повесим обработчик на событие построения маршрута.
        route.model.events.add('requestsuccess', function () {

            var activeRoute = route.getActiveRoute();
            if (activeRoute) {
                // Получим протяженность маршрута.
                var length = route.getActiveRoute().properties.get("distance"),
                // Вычислим стоимость доставки.
                    price = calculate(Math.round(length.value / 1000)),
                // Создадим макет содержимого балуна маршрута.
                    balloonContentLayout = ymaps.templateLayoutFactory.createClass(
                        '<span>Расстояние: ' + length.text + '.</span><br/>' +
                        '<span style="font-weight: bold; font-style: italic">Стоимость поездки: ' + price + ' р.</span>');
                // Зададим этот макет для содержимого балуна.
                route.options.set('routeBalloonContentLayout', balloonContentLayout);
                // Откроем балун.
                activeRoute.balloon.open();
            }
        });

    });
    // Функция, вычисляющая стоимость доставки.
    function calculate(routeLength) {
        return Math.max(routeLength * DELIVERY_TARIFF, MINIMUM_COST);
    }

// Создаем круг.
    var myCircle = new ymaps.Circle([
    // Координаты центра круга.
    [51.66114505, 39.20129184],
    // Радиус круга в метрах.
    8000
], {
    // Описываем свойства круга.
    // Содержимое балуна.
    balloonContent: "Радиус круга - 8 км",
    // Содержимое хинта.
    hintContent: "Подвинь меня"
}, {
    // Задаем опции круга.
    // Включаем возможность перетаскивания круга.
    draggable: false,
    // Цвет заливки.
    // Последний байт (77) определяет прозрачность.
    // Прозрачность заливки также можно задать используя опцию "fillOpacity".
    fillOpacity: 0.2,
    fillColor: "#fdd99b",
    // Цвет обводки.
    strokeColor: "#ff7f50",
    // Прозрачность обводки.
    strokeOpacity: 0.3,
    // Ширина обводки в пикселях.
    strokeWidth: 5
});

// Добавляем круг на карту.
myMap.geoObjects.add(myCircle);
}




