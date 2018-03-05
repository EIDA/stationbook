var latitude = parseFloat("{{ station.latitude }}");
var longitude = parseFloat("{{ station.longitude }}");
var siteCode = "{{ station.code }}"
var markerPath = "{% static 'img/markers/marker-red.png' %}"

map.getView().setCenter(ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857'));
map.getView().setZoom(10);

// Check if values are valid and add a marker to the map
if (!isNaN(latitude) && !isNaN(longitude)) {
    var point = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([longitude, latitude])),
        name: `<b>Site code: </b>${siteCode}
        <br><b>Latitude: </b>${latitude}
        <br><b>Longitude: </b>${longitude}`
    });

    point.setStyle(new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: markerPath,
        }))
    }));
    vectorSource.addFeature(point);
}