function getToken() {

    return localStorage.getItem("access");

}


async function loadWallet() {

    try {

        const token = getToken();

        const response =
        await fetch(
            "/recharge/api/wallet/",
            {
                headers: {
                    Authorization:
                    `Bearer ${token}`
                }
            }
        );

        const data =
        await response.json();

        const wallet =
        document.getElementById(
            "walletBalance"
        );

        if(wallet){

            wallet.innerText =
            data.balance;

        }

    }

    catch(error){

        console.log(error);

    }

}

async function loadTransactions() {

    try {

        const token =
        getToken();

        if (!token) {

            console.log(
                "No access token found"
            );

            return;

        }

        const response =
        await fetch(

            "/recharge/api/my-recharges/",

            {

                method: "GET",

                headers: {

                    Authorization:
                    `Bearer ${token}`

                }

            }

        );

        const data =
        await response.json();

        const table =
        document.getElementById(
            "transactionTableBody"
        );

        if (!table) {

            console.log(
                "transactionTableBody missing"
            );

            return;

        }

        table.innerHTML = "";

        let totalAmount = 0;
        let totalCashback = 0;
        let totalSuccess = 0;

        data.forEach(item => {

            totalAmount +=
            parseFloat(item.amount);

            totalCashback +=
            parseFloat(item.cashback);

            if (
                item.status === "success"
            ) {

                totalSuccess++;

            }

            const statusClass =

                item.status === "success"

                ? "status-success"

                :

                item.status === "failed"

                ? "status-failed"

                :

                "status-pending";

            table.innerHTML += `

                <tr>

                    <td>

                        ${new Date(
                            item.created_at
                        ).toLocaleDateString()}

                    </td>

                    <td>

                        ${item.provider}

                    </td>

                    <td>

                        ${item.mobile_number}

                    </td>

                    <td>

                        ₹${item.amount}

                    </td>

                    <td class="cashback">

                        ₹${item.cashback}

                    </td>

                    <td
                    class="${statusClass}"
                    >

                        ${item.status}

                    </td>

                    <td>

                        ${item.transaction_id}

                        <br>

                        <button

                        class="copy-btn"

                        onclick="copyTxn(
                            '${item.transaction_id}'
                        )"

                        >

                        Copy

                        </button>

                    </td>

                </tr>

            `;

        });

        document.getElementById(
            "totalTransactions"
        ).innerText =
        data.length;

        document.getElementById(
            "totalAmount"
        ).innerText =
        "₹" +
        totalAmount.toFixed(2);

        document.getElementById(
            "totalCashback"
        ).innerText =
        "₹" +
        totalCashback.toFixed(2);

        document.getElementById(
            "totalSuccess"
        ).innerText =
        totalSuccess;

    }

    catch(error) {

        console.log(error);

    }

}

function copyTxn(txn) {

    navigator.clipboard.writeText(
        txn
    );

    alert(
        "Transaction ID copied"
    );

}

function searchTransactions() {

    const value =

    document
    .getElementById(
        "searchInput"
    )
    .value
    .toLowerCase();

    const rows =

    document.querySelectorAll(
        "#transactionTableBody tr"
    );

    rows.forEach(row => {

        row.style.display =

        row.innerText
        .toLowerCase()
        .includes(value)

        ? ""

        : "none";

    });

}

document.addEventListener(

    "DOMContentLoaded",

    function(){

        loadTransactions();

        loadWallet();

    }

);