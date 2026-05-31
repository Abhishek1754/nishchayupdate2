javascript
function getToken() {

    return localStorage.getItem(
        "access"
    );

}

/* ===========================
   WALLET SUMMARY
=========================== */

async function loadWalletSummary() {

    try {

        const token =
        getToken();

        const response =
        await fetch(

            "/recharge/api/wallet/",

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

        document.getElementById(
            "walletBalance"
        ).innerText =
        "₹" +
        (data.balance || 0);

    }

    catch(error){

        console.log(error);

    }

}

/* ===========================
   WALLET HISTORY
=========================== */

async function loadWalletHistory() {

    try {

        const token =
        getToken();

        if(!token){

            console.log(
                "JWT token missing"
            );

            return;

        }

        const response =
        await fetch(

            "/recharge/api/wallet-history/",

            {

                method:"GET",

                headers:{

                    Authorization:
                    `Bearer ${token}`

                }

            }

        );

        const data =
        await response.json();

        const tableBody =
        document.getElementById(
            "walletTableBody"
        );

        tableBody.innerHTML = "";

        if(
            !Array.isArray(data)
        ){

            console.log(data);

            return;

        }

        let totalCredits = 0;
        let totalDebits = 0;
        let cashbackEarned = 0;

        if(data.length === 0){

            tableBody.innerHTML = `

                <tr>

                    <td
                    colspan="4"
                    class="empty-state"
                    >

                    No wallet transactions found

                    </td>

                </tr>

            `;

        }

        data.forEach(item => {

            const amount =
            parseFloat(
                item.amount
            );

            let badgeClass =
            "credit";

            let amountClass =
            "amount-credit";

            if(
                item.transaction_type
                ===
                "debit"
            ){

                badgeClass =
                "debit";

                amountClass =
                "amount-debit";

                totalDebits +=
                amount;

            }

            else{

                totalCredits +=
                amount;

                if(

                    item.message
                    .toLowerCase()
                    .includes(
                        "cashback"
                    )

                ){

                    cashbackEarned +=
                    amount;

                }

            }

            tableBody.innerHTML += `

                <tr>

                    <td>

                        ${new Date(
                            item.created_at
                        ).toLocaleDateString()}

                    </td>

                    <td>

                        <span
                        class="${badgeClass}"
                        >

                        ${item.transaction_type}

                        </span>

                    </td>

                    <td
                    class="${amountClass}"
                    >

                        ₹${item.amount}

                    </td>

                    <td>

                        ${item.message}

                    </td>

                </tr>

            `;

        });

        document.getElementById(
            "totalCredits"
        ).innerText =
        "₹" +
        totalCredits.toFixed(2);

        document.getElementById(
            "totalDebits"
        ).innerText =
        "₹" +
        totalDebits.toFixed(2);

        document.getElementById(
            "cashbackEarned"
        ).innerText =
        "₹" +
        cashbackEarned.toFixed(2);

    }

    catch(error){

        console.log(error);

    }

}

/* ===========================
   SEARCH
=========================== */

function searchWalletHistory(){

    const searchValue =

    document
    .getElementById(
        "searchInput"
    )
    .value
    .toLowerCase();

    const rows =

    document.querySelectorAll(
        "#walletTableBody tr"
    );

    rows.forEach(row => {

        row.style.display =

        row.innerText
        .toLowerCase()
        .includes(searchValue)

        ? ""

        : "none";

    });

}

/* ===========================
   INIT
=========================== */

document.addEventListener(

    "DOMContentLoaded",

    function(){

        loadWalletSummary();

        loadWalletHistory();

    }

)
