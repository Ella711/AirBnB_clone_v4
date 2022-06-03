window.onload =

function init () {
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
};
