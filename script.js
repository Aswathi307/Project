let total = 0;

async function addToBill() {
    const id = document.getElementById("productId").value.trim();
    const qty = parseInt(document.getElementById("quantity").value) || 1;

    try {
        const response = await fetch(`http://localhost:3000/product/${id}`);

        if (!response.ok) {
            alert("Product not found!");
            return;
        }

        const product = await response.json();
        const cost = product.price * qty;

        const table = document.getElementById("billTable");
        const row = table.insertRow();

        row.insertCell(0).innerText = product.name;
        row.insertCell(1).innerText = product.price;
        row.insertCell(2).innerText = qty;
        row.insertCell(3).innerText = cost;

        // Remove button
        const removeCell = row.insertCell(4);
        const btn = document.createElement("button");
        btn.innerText = "Remove";
        btn.className = "remove-btn";

        btn.onclick = function () {
            total -= cost;
            document.getElementById("total").innerText = total;
            table.deleteRow(row.rowIndex);
        };

        removeCell.appendChild(btn);

        // ✅ Correct total update
        total += cost;
        document.getElementById("total").innerText = total;

    } catch (error) {
        alert("Backend not running!");
    }

    document.getElementById("productId").value = "";
    document.getElementById("quantity").value = "";
}