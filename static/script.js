function formatRupiah(input) {

    let angka = input.value.replace(/\D/g, "");

    input.value = angka.replace(
        /\B(?=(\d{3})+(?!\d))/g,
        "."
    );
}

document.addEventListener("DOMContentLoaded", () => {

    const budget =
        document.getElementById("budget");

    const harga =
        document.getElementById("harga");

    if (budget) {
        budget.addEventListener(
            "input",
            () => formatRupiah(budget)
        );
    }

    if (harga) {
        harga.addEventListener(
            "input",
            () => formatRupiah(harga)
        );
    }

});