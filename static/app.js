// // app.js

// // Register form submit
// const registerForm = document.getElementById("registerForm");
// if (registerForm) {
//     registerForm.addEventListener("submit", async (e) => {
//         e.preventDefault();

//         const username = document.getElementById("regUsername").value;
//         const password = document.getElementById("regPassword").value;

//         const res = await fetch("/register", {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ username, password })
//         });

//         const data = await res.json();
//         alert(data.message);
//     });
// }

// // Login form submit
// const loginForm = document.getElementById("loginForm")
