function filter_ports(filter) {
  let portCol = document.querySelectorAll("tbody tr td:last-child");
  portCol.forEach((item) => {
    if(!new RegExp(filter).test(item.innerText)){
      item.parentNode.style.display = "none";
    } else {
      item.parentNode.style.display = "table-row";
    }
  });
}

document.querySelector("#ports").addEventListener("keyup", (event) => {
  if (event.key === "Enter") {
    filter_ports(event.srcElement.value);
  }
});

function count_rows() {
  return document.querySelectorAll('tr:not([style*="display:none"]):not([style*="display: none"])').length;
}