
const amenitiesDict = {};
const checkbox = document.querySelector('.amenities .popover input');
checkbox.change(function () {
  const amenity = document.querySelector(this);
  if (amenity.is(':checked')) {
    amenitiesDict[amenity.attr('data-name')] = amenity.attr('data-id');
  } else if (amenity.is(':not(:checked)')) {
    delete amenitiesDict[amenity.attr('data-name')];
  }
  const names = Object.keys(amenitiesDict);
  const amenitiesH4 = document.querySelector('.amenities h4');
  amenitiesH4.text(names.sort().join(', '));
});

const URL = 'http://0.0.0.0:5001/api/v1/status/';
const apiStatus = document.querySelector('#api_status');
$.get(URL, (data, headerStatus) => {
  if (headerStatus === 'success' && data.status === 'OK') {
    apiStatus.classList.add('available');
  } else {
    apiStatus.classList.remove('available');
  }
});
