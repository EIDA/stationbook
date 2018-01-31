var map = new ol.Map({
    target: 'map',
      layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM()
    }
    )
    ],
    controls: ol.control.defaults({
      attributionOptions: {
        collapsible: false
      }
    }
    ),
    target: 'map',
      view: new ol.View({
        center: ol.proj.fromLonLat([5.178029, 52.101568]),
          zoom: 16
    }
    )
  }
  );
  var source = new ol.source.Vector({
    wrapX: false
  }
  );
  var vector = new ol.layer.Vector({
    source: source
  }
  );
  map.addLayer(vector);
  