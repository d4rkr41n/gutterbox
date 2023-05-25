function get_displayed_rows() {
  return document.querySelectorAll('tbody tr:not([style*="display:none"]):not([style*="display: none"])');
}

function count_rows() {
  return get_displayed_rows().length;
}

document.querySelector(".result-count").addEventListener("click", function() {
  var addresses = [];
  get_displayed_rows().forEach((element) => {
    addresses.push( element.querySelector("td:nth-child(3)").innerText );
  });
  navigator.clipboard.writeText(addresses.join('\n'));
});
