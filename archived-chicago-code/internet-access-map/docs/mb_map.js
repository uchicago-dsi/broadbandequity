const colors = ['#800000', '#b81414', '#d13400', '#ffcd38', '#ffff33'];
const ncolors = colors.length;

class DataLayer {
 constructor(tag, label, descr, data, stops) {
   this.tag    = tag;
   this.label  = label;
   this.descr  = descr;
   this.data   = data;
   this.stops  = stops;
 }
}

class DataSource {
 constructor(tag, label, descr, url) {
   this.tag    = tag;
   this.label  = label;
   this.descr  = descr;
   this.url    = url;
 }
}

data_sources = {
  "acs"   : new DataSource("acs",   "US Census",       "American Community Survey", "https://www.census.gov/programs-surveys/acs/about.html"),
  "fcc"   : new DataSource("fcc",   "FCC Form 477",    "FCC Form 477",              "https://www.fcc.gov/general/broadband-deployment-data-fcc-form-477"),
  "ookla" : new DataSource("ookla", "Ookla Speedtest", "Speedtest by Ookla",        "https://registry.opendata.aws/speedtest-global-performance/")
}

source_names = ["acs", "fcc", "ookla"];


data_layers = {
  "f_broadband"          : new DataLayer("f_broadband", "Broadband Access", "Frac. of Households with Broadband Subscription", "acs", [ 0.6, 0.7, 0.8, 0.9, 1.0]), 
  "f_computer"           : new DataLayer("f_computer", "Computer in HH", "Frac. of Households </br>with a Computer", "acs", [0.6, 0.7, 0.8, 0.9, 1.0]),
  "f_ba"                 : new DataLayer("f_ba", "Frac. College Grads", "Frac. of Adult</br>Population with a BA", "acs", [0.0, 0.25, 0.50, 0.75, 1.00]),
  "f_black"              : new DataLayer("f_black", "Frac. Black", "Share of Population</br>that is Black", "acs", [0.0, 0.25, 0.50, 0.75, 1.00]),
  "f_hispanic"           : new DataLayer("f_hispanic", "Frac. Hispanic", "Share of Population</br>that is Hispanic", "acs", [0.0, 0.25, 0.50, 0.75, 1.00]),
  "log_mhi"              : new DataLayer("log_mhi", "Log Income", "Log. of Median</br>Household Income", "acs", [10, 10.5, 11, 11.5, 12]),
  "n_isp"                : new DataLayer("n_isp", "# of ISPs", "Number of ISPs", "fcc", [0, 1, 2, 3, 4]),
  "n_dn10"               : new DataLayer("n_dn10", "ISPs @ 10 Mbps", "# of ISPs with &gt; 10 Mbps Downstream", "fcc", [0, 1, 2, 3, 4]),
  "n_dn100"              : new DataLayer("n_dn100", "ISPs @ 100 Mbps", "# of ISPs with &gt; 100 Mbps Downstream", "fcc", [0, 1, 2, 3, 4]),
  "n_dn250"              : new DataLayer("n_dn250", "ISPs @ 250 Mbps", "# of ISPs with &gt; 250 Mbps Downstream", "fcc", [0, 1, 2, 3, 4]),
  "n_fiber_100u"         : new DataLayer("n_fiber_100u", "Fiber ISPs @ 100 Up", "# Fiber Offerings with Upstream &gt; 100 Mbps", "fcc", [0, 1, 2, 3, 4]),
  "fiber_100u_exists"    : new DataLayer("fiber_100u_exists", "Fiber Availability", "Share of Blocks with Fiber", "fcc", [0, 0.25, 0.50, 0.75, 1.00]),
  "max_dn"               : new DataLayer("max_dn", "Max Adv. Downstream", "Max Available</br>Downstream Speed", "fcc", [0, 25, 100, 500, 1000]),
  "max_up"               : new DataLayer("max_up", "Max Adv. Upstream", "Max Available</br>Upstream Speed", "fcc", [0, 25, 100, 500, 1000]),
  "d_mbps"               : new DataLayer("d_mbps", "Avg. Download Rate", "Average Fixed-Line Downstream Speed [Mbps]", "ookla", [0, 25, 100, 200, 300]),
  "u_mbps"               : new DataLayer("u_mbps", "Avg. Upload Rate", "Average Fixed-Line Upstream Speed [Mbps]", "ookla", [0, 10, 30, 50, 150]),
  "lat_ms"               : new DataLayer("lat_ms", "Avg. Latency", "Average Fixed-Line</br>Latency [ms]", "ookla", [0, 10, 25, 50, 100]),
  "tests_per_cap"        : new DataLayer("tests_per_cap", "Tests per Capita", "Ookla Tests, Per Capita", "ookla", [0, 0.01, 0.025, 0.05, 0.10]),
  "devices_per_cap"      : new DataLayer("devices_per_cap", "Devices per Capita", "Devices Running Ookla Test, Per Capita", "ookla", [0, 0.01, 0.02, 0.03, 0.05])
}


/// MAPBOX STUFF...

// define access token
mapboxgl.accessToken = 'pk.eyJ1IjoibWFyY3dpdGFzZWUiLCJhIjoiY2tkaHljOHNqMDB3dDJ3cGI2dWR2YmpuaSJ9.thA8fs03yFEs88QIdFs2Og';

// create map
const map = new mapboxgl.Map({
  container: 'map', // container id
  style: 'mapbox://styles/marcwitasee/cl2utne3n001915nwzo505ass', // map style URL from Mapbox Studio
  zoom: 9.5,
  center: [-87.672, 41.839],
  minZoom: 5.01,
  maxZoom: 17,
  attributionControl: false
});

map.dragRotate.disable();
map.touchZoomRotate.disableRotation();

map.addControl(new mapboxgl.AttributionControl({
  customAttribution: '</br>Data from US Census <a href=https://www.census.gov/programs-surveys/acs/about.html>American Community Survey</a>, <a href=https://opendata.fcc.gov/Wireline/Fixed-Broadband-Deployment-Data-Jun-2019-Status-V1/sgz3-kiqt>FCC Form 477</a>, and <a href=https://registry.opendata.aws/speedtest-global-performance/>Speedtest by Ookla</a>.</br>Map design by <a href=https://saxon.cdac.uchicago.edu>James Saxon</a>, <a href=http://datascience.uchicago.edu>Data Science Institute</a>, <a href=http://www.uchicago.edu>University of Chicago</a>, &copy; 2022.'
}));


var legend_header = null;
var legend_val = [];
var var_select = null;
var data_text = null;

set_map_color = function () {

  paint_var = var_select.value;

  dl = data_layers[paint_var];

  legend_header.innerHTML = dl.descr;

  paint_prop = ['interpolate', ['linear']];
  paint_prop.push(["get", dl.tag]);

  for (var i = 0; i < dl.stops.length; i++) {
    paint_prop.push(dl.stops[i]);
    paint_prop.push(colors[i]);

    legend_val[i].innerHTML = dl.stops[i];
    if (i == ncolors-1 && dl.stops[i] != 1) {
      legend_val[i].innerHTML += "+";
    }
  }

  map.setPaintProperty("broadband", "fill-color", paint_prop);

  ds = data_sources[dl.data];
  data_text.innerHTML = `Data: <a href='${ds.url}'>${ds.label}</a>`;

}

var paint_var = "d_mbps";


function in_frame () {

  try {
    return window.self !== window.top;
  } catch (e) {
    return true;
  }

}


// wait for map to load before adjusting it
map.on('load', () => {

  // make a pointer cursor
  map.getCanvas().style.cursor = 'default';


  // create legend
  // const legend = document.getElementById('legend');
  const legend = document.createElement('div');
  legend.id = "legend";
  legend.className = "map-overlay";

  document.body.appendChild(legend);

  // First the selector.
  var_select = document.createElement('select');
  var_select.id = "varselect";
  var_select.onchange = set_map_color;
  legend.appendChild(var_select);

  source_names.forEach(function (src) {

      group = document.createElement('optgroup');
      group.label = data_sources[src].label;
      var_select.appendChild(group);

      for (var key in data_layers) {
        dl = data_layers[key];
        if (dl.data != src) continue;

        const opt = document.createElement('option');
        opt.value = dl.tag;
        opt.innerHTML = dl.label;

        if (dl.tag == "f_broadband") opt.selected = true;

        group.appendChild(opt);

      }
  });

  legend.appendChild(document.createElement('hr'));

  // Now create the key / color area -- 
  
  // First the variable description
  const title_div = document.createElement('div');
  legend_header= document.createElement('h3');

  legend_header.innerHTML = dl.descr;
  title_div.appendChild(legend_header);
  legend.appendChild(title_div);

  legend.appendChild(document.createElement('hr'));

  // Next the legend itself, using a table...
  const legend_table = document.createElement('table');
  legend_table.id = 'legend-table';
  legend.appendChild(legend_table);

  const legend_body = document.createElement('tb');
  legend_table.appendChild(legend_body);

  dl = data_layers[paint_var];

  dl.stops.forEach((layer, i) => {

    const row = document.createElement('tr');
    color_cell = document.createElement('td');
    color_cell.className = 'legend-colors';
    color_cell.style.backgroundColor = colors[i]

    const value_cell = document.createElement('td');
    value_cell.innerHTML = `${layer}`;
    value_cell.className = 'legend-value';
    if (i == ncolors-1) value_cell.innerHTML += "+"; 
    legend_val.push(value_cell);

    row.appendChild(color_cell);
    row.appendChild(value_cell);
    legend_body.appendChild(row);
  });

  legend.appendChild(document.createElement('hr'));

  const data_div = document.createElement('div');
  data_text = document.createElement('p');
  
  ds = data_sources[dl.data];
  data_text.id = "data_ref";
  data_text.innerHTML = `Data: <a href='${ds.url}'>${ds.label}</a>`;
  data_div.appendChild(data_text);
  legend.appendChild(data_div);

  const dl_div = document.createElement('div');
  dl_text = document.createElement('p');

  dl_text.id = "dl_ref";
  // TODO: Update href with new web domain for hosting map
  dl_text.innerHTML = "Download <a href='/~jsaxon/us_map/uchicago_broadband_data.csv.gz'>&#x2B07</a>";
  dl_div.appendChild(dl_text);
  legend.appendChild(dl_div);


  // Do this here, only after the legend is available.
  set_map_color(paint_var);

  var is_in_frame = in_frame();

  if (is_in_frame) {

    value_header = document.getElementById('value_header');
    value_div    = document.getElementById('value_div');

    value_header.innerHTML = "";

    const full_screen = document.createElement('a');
    full_screen.href = "https://chicago-cdac.github.io/internet-access-map/";
    full_screen.target = "_blank";
    full_screen.innerHTML = "Full Screen &#x27A1;";
    value_header.appendChild(full_screen);

    value_div.innerHTML = "";

  } else {

    // change info window on hover
    map.on('mousemove', (event) => {
      const tract = map.queryRenderedFeatures(event.point, { layers: ['broadband'] });

      value_header = document.getElementById('value_header');
      value_div    = document.getElementById('value_div');

      if (tract.length == 0) { 
        value_header.innerHTML = "Hover for values.";
        value_div.innerHTML = "";

      } else {

        value_div.innerHTML = "";

        props = tract[0].properties;
        value_header.innerHTML = `Tract ${props.geoid}`;

        const value_table = document.createElement('table');
        value_table.id = 'value-table';
        value_div.appendChild(value_table);

        const value_body = document.createElement('tb');
        value_table.appendChild(value_body);

        for (var key in data_layers) {

          dl = data_layers[key];

          const row = document.createElement('tr');

          label_cell = document.createElement('td');
          label_cell.innerHTML = dl.label;

          value_cell = document.createElement('td');
          if (props[key] == null) {
            value_cell.innerHTML = "--";
          } else {
            value_cell.innerHTML = props[key];
          }

          row.appendChild(label_cell);
          row.appendChild(value_cell);
          value_body.appendChild(row);

        }

      }
    });

  }

});



