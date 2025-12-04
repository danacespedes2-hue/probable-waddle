document.addEventListener("DOMContentLoaded", () => {
	const cartCountElement = document.getElementById("cart-count");
	const cartButton = document.getElementById("cart-button");

	const modal = document.getElementById("payment-modal");
	const closeModalBtn = document.getElementById("close-modal");

	const summaryBody = document.getElementById("summary-body");
	const summaryTotal = document.getElementById("summary-total");

	const paymentForm = document.getElementById("payment-form");
	const modalBodyPayment = document.getElementById("modal-body-payment");
	const modalBodyTicket = document.getElementById("modal-body-ticket");

	const ticketId = document.getElementById("ticket-id");
	const ticketDate = document.getElementById("ticket-date");
	const ticketName = document.getElementById("ticket-name");
	const ticketItems = document.getElementById("ticket-items");
	const ticketTotal = document.getElementById("ticket-total");
	const btnNewOrder = document.getElementById("btn-new-order");
	const btnPrintTicket = document.getElementById("btn-print-ticket");

	let cartCount = 0;
	let cart = []; // { name, price }

	/* ====== AÑADIR PRODUCTOS AL CARRITO ====== */
	const productCards = document.querySelectorAll(".card-product");
	productCards.forEach(card => {
		const addButton = card.querySelector(".add-cart");
		if (!addButton) return;

		addButton.addEventListener("click", () => {
			const nameEl = card.querySelector("h3");
			const priceEl = card.querySelector(".price");

			const name = nameEl ? nameEl.textContent.trim() : "Producto";
			let price = 0;
			if (priceEl) {
				const match = priceEl.textContent.match(/(\d+(\.\d+)?)/);
				if (match) {
					price = parseFloat(match[1]);
				}
			}

			cart.push({ name, price });
			cartCount++;
			cartCountElement.textContent = `(${cartCount})`;
		});
	});

	/* ====== MODAL PAGO ====== */
	cartButton.addEventListener("click", () => {
		if (cart.length === 0) {
			alert("Tu carrito está vacío.");
			return;
		}
		fillSummary();
		modal.classList.add("show");
		modalBodyPayment.style.display = "block";
		modalBodyTicket.style.display = "none";
	});

	closeModalBtn.addEventListener("click", () => {
		modal.classList.remove("show");
	});
	modal.addEventListener("click", (e) => {
		if (e.target === modal) {
			modal.classList.remove("show");
		}
	});

	function fillSummary() {
		summaryBody.innerHTML = "";
		let total = 0;

		cart.forEach(item => {
			const tr = document.createElement("tr");
			const tdName = document.createElement("td");
			const tdPrice = document.createElement("td");

			tdName.textContent = item.name;
			tdPrice.textContent = `$${item.price.toFixed(2)}`;
			tdPrice.classList.add("text-right");

			tr.appendChild(tdName);
			tr.appendChild(tdPrice);
			summaryBody.appendChild(tr);

			total += item.price;
		});

		summaryTotal.textContent = `$${total.toFixed(2)}`;
	}

	paymentForm.addEventListener("submit", (e) => {
		e.preventDefault();

		const name = document.getElementById("customer-name").value.trim();
		const email = document.getElementById("customer-email").value.trim();
		const method = document.getElementById("payment-method").value;

		if (!name || !email) {
			alert("Por favor, llena nombre y correo.");
			return;
		}

		showTicket(name, email, method);
	});

	function showTicket(name, email, method) {
		const now = new Date();
		const folio = "BAR-" + now.getTime().toString(36).toUpperCase();

		ticketId.textContent = folio;
		ticketDate.textContent = now.toLocaleString();
		ticketName.textContent = name + " (" + email + ")";

		ticketItems.innerHTML = "";
		let total = 0;
		cart.forEach(item => {
			const tr = document.createElement("tr");
			const tdName = document.createElement("td");
			const tdPrice = document.createElement("td");

			tdName.textContent = item.name;
			tdPrice.textContent = `$${item.price.toFixed(2)}`;
			tdPrice.classList.add("text-right");

			tr.appendChild(tdName);
			tr.appendChild(tdPrice);
			ticketItems.appendChild(tr);

			total += item.price;
		});

		ticketTotal.textContent = `$${total.toFixed(2)} (${method})`;

		modalBodyPayment.style.display = "none";
		modalBodyTicket.style.display = "block";
	}

	btnNewOrder.addEventListener("click", () => {
		cart = [];
		cartCount = 0;
		cartCountElement.textContent = "(0)";
		modal.classList.remove("show");
		paymentForm.reset();
	});

	btnPrintTicket.addEventListener("click", () => {
		window.print();
	});

	/* ====== CATEGORÍAS INTERACTIVAS ====== */
	const categoryCards = document.querySelectorAll(".card-category");
	const allProducts = document.querySelectorAll(".container-products .card-product");
	const topProductsSection = document.querySelector(".top-products");

	function filterProducts(filter) {
		allProducts.forEach(card => {
			const cat = card.dataset.category;
			if (!filter || filter === "all" || cat === filter) {
				card.style.display = "flex";
			} else {
				card.style.display = "none";
			}
		});
	}

	categoryCards.forEach(card => {
		card.addEventListener("click", () => {
			const filter = card.dataset.filter;

			categoryCards.forEach(c => c.classList.remove("active-category"));
			card.classList.add("active-category");

			filterProducts(filter);

			if (topProductsSection) {
				const top = topProductsSection.offsetTop - 80;
				window.scrollTo({ top, behavior: "smooth" });
			}
		});
	});

	// Inicialmente mostrar todo
	filterProducts("all");
});
