window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

// const delete_button = document.getElementById("delete_button");

// delete_button.addEventListener("click", async e => {
//   console.log(e);
//   const id = e.target.dataset.id;

//   await fetch("/venues/" + id, {
//     method: "DELETE",
//     headers: {
//       "Content-Type": "application/json",
//       // 'Content-Type': 'application/x-www-form-urlencoded',
//     },
//   });
// });
