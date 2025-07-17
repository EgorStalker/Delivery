 function updateStatus() {
            const id = document.getElementById("packageId").value;
            const status = document.getElementById("newStatus").value;

            fetch(`/a/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ status_package: status })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("result").innerText = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                document.getElementById("result").innerText = "Ошибка: " + error;
            });
        }