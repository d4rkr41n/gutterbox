function get_displayed_rows() {
  return document.querySelectorAll('tbody tr:not([style*="display:none"]):not([style*="display: none"])');
}

function count_rows() {
  return get_displayed_rows().length;
}

// Add toggle listener for row clicks
document.querySelectorAll("tbody tr").forEach((row) => {
  row.addEventListener("click", function() {
    row.classList.toggle('active');
  });
});

// Add listener for copy addresses from query
document.querySelector(".result-count").addEventListener("click", function() {
  var addresses = [];
  get_displayed_rows().forEach((element) => {
    addresses.push( element.querySelector("td:nth-child(3)").innerText );
  });
  navigator.clipboard.writeText(addresses.join('\n'));
});
