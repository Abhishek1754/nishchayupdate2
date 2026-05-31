function getToken() {

    return localStorage.getItem("access");

}

/* =========================================
   AUTH HEADERS
========================================= */

function authHeaders(isJson = true) {

    const token = getToken();

    const headers = {};

    if (token) {

        headers["Authorization"] =
        `Bearer ${token}`;

    }

    if (isJson) {

        headers["Content-Type"] =
        "application/json";

    }

    return headers;

}

/* =========================================
   TOAST NOTIFICATION
========================================= */

function showToast(message, type = "success") {

    const existing =
    document.querySelector(".toast");

    if (existing) {

        existing.remove();

    }

    const toast =
    document.createElement("div");

    toast.className =
    `toast ${type}`;

    toast.innerHTML = `

        <div class="toast-inner">

            <span class="toast-icon">

                ${type === "success" ? "✅" : "❌"}

            </span>

            <span class="toast-text">

                ${message}

            </span>

        </div>

    `;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.classList.remove("show");

        setTimeout(() => {

            toast.remove();

        }, 500);

    }, 3500);

}

/* =========================================
   ANIMATE WALLET
========================================= */

function animateValue(elementId, start, end, duration) {

    let startTimestamp = null;

    const step = (timestamp) => {

        if (!startTimestamp)
            startTimestamp = timestamp;

        const progress =
        Math.min(
            (timestamp - startTimestamp)
            / duration,
            1
        );

        const value =
        Math.floor(
            progress *
            (end - start) +
            start
        );

        document.getElementById(
            elementId
        ).innerText = value;

        if (progress < 1) {

            window.requestAnimationFrame(step);

        }

    };

    window.requestAnimationFrame(step);

}

/* =========================================
   LOAD WALLET
========================================= */

async function loadWallet() {

    try {

        const response = await fetch(
            "/recharge/api/wallet/",
            {
                method: "GET",
                headers: authHeaders(false)
            }
        );

        const data = await response.json();

        console.log("Wallet API:", data);

        const balance = parseFloat(
            data.balance || 0
        );

        const wallet1 =
        document.getElementById(
            "walletBalance"
        );

        const wallet2 =
        document.getElementById(
            "walletBalance2"
        );

        if(wallet1){

            wallet1.innerText =
            balance.toFixed(2);

        }

        if(wallet2){

            wallet2.innerText =
            balance.toFixed(2);

        }

    }

    catch(error){

        console.log(
            "Wallet Error:",
            error
        );

    }

}

/* =========================================
   LOAD PROVIDERS
========================================= */

async function loadProviders() {

    try {

        const response =
        await fetch(
            "/recharge/api/providers/"
        );

        const data =
        await response.json();

        const providerSelect =
        document.getElementById(
            "provider"
        );

        providerSelect.innerHTML = "";

        data.forEach(provider => {

            providerSelect.innerHTML += `

                <option value="${provider.id}">
                    ${provider.name}
                </option>

            `;

        });

    } catch (error) {

        console.log(error);

    }

}

/* =========================================
   LOAD COUPONS
========================================= */

async function loadCoupons() {

    try {

        const response =
        await fetch(
            "/recharge/api/coupons/"
        );

        const data =
        await response.json();

        const couponContainer =
        document.getElementById(
            "couponContainer"
        );

        couponContainer.innerHTML = "";

        if (data.length === 0) {

            couponContainer.innerHTML = `

                <div class="empty-offer">

                    No cashback offers available

                </div>

            `;

            return;

        }

        data.forEach(coupon => {

            couponContainer.innerHTML += `

                <div class="offer-card">

                    <div class="offer-top">

                        <span class="offer-badge">
                            Cashback
                        </span>

                        <span class="offer-percent">
                            ${coupon.cashback_percentage}%
                        </span>

                    </div>

                    <h3>
                        ${coupon.title}
                    </h3>

                    <p>
                        Use this coupon while recharging
                        to get instant cashback.
                    </p>

                    <div class="coupon-code">

                        ${coupon.code}

                    </div>

                </div>

            `;

        });

    } catch (error) {

        console.log(error);

    }

}

/* =========================================
   DO RECHARGE
========================================= */

async function doRecharge() {

    const provider =
    document.getElementById(
        "provider"
    ).value;

    const mobile =
    document.getElementById(
        "mobile"
    ).value;

    const amount =
    document.getElementById(
        "amount"
    ).value;

    const token =
    getToken();

    if (!token) {

        showToast(
            "Please login first",
            "error"
        );

        return;

    }

    if (!mobile || !amount) {

        showToast(
            "Please fill all fields",
            "error"
        );

        return;

    }

    const rechargeBtn =
    document.querySelector(
        ".recharge-btn"
    );

    try {

        rechargeBtn.disabled = true;

        rechargeBtn.innerHTML = `

            <span class="loader"></span>
            Processing...

        `;

        const response =
        await fetch(
            "/recharge/api/do-recharge/",
            {

                method: "POST",

                headers:
                authHeaders(),

                body: JSON.stringify({

                    provider_id: provider,
                    mobile_number: mobile,
                    amount: amount

                })

            }
        );

        const data =
        await response.json();

        rechargeBtn.disabled = false;

        rechargeBtn.innerHTML =
        "⚡ Recharge Now";

        if (response.ok) {

            showToast(
                data.message ||
                "Recharge Successful"
            );

            document.getElementById(
                "mobile"
            ).value = "";

            document.getElementById(
                "amount"
            ).value = "";

            loadWallet();

            launchConfetti();

            showSuccessModal(
                mobile,
                amount
            );

        } else {

            showToast(
                data.message ||
                "Recharge Failed",
                "error"
            );

        }

    } catch (error) {

        console.log(error);

        rechargeBtn.disabled = false;

        rechargeBtn.innerHTML =
        "⚡ Recharge Now";

        showToast(
            "Server Error",
            "error"
        );

    }

}

/* =========================================
   SUCCESS MODAL
========================================= */

function showSuccessModal(mobile, amount) {

    const modal =
    document.createElement("div");

    modal.className =
    "success-modal";

    modal.innerHTML = `

        <div class="success-box">

            <div class="success-animation">

                ✅

            </div>

            <h2>
                Recharge Successful
            </h2>

            <div class="success-details">

                <div class="success-row">

                    <span>Mobile</span>

                    <strong>${mobile}</strong>

                </div>

                <div class="success-row">

                    <span>Amount</span>

                    <strong>₹${amount}</strong>

                </div>

            </div>

            <button
                class="success-btn"
                onclick="closeSuccessModal()"
            >
                Continue
            </button>

        </div>

    `;

    document.body.appendChild(modal);

}

function closeSuccessModal() {

    const modal =
    document.querySelector(
        ".success-modal"
    );

    if (modal) {

        modal.remove();

    }

}

/* =========================================
   CONFETTI EFFECT
========================================= */

function launchConfetti() {

    for (let i = 0; i < 40; i++) {

        const confetti =
        document.createElement("div");

        confetti.className =
        "confetti";

        confetti.style.left =
        Math.random() * 100 + "vw";

        confetti.style.animationDuration =
        (Math.random() * 2 + 2) + "s";

        document.body.appendChild(confetti);

        setTimeout(() => {

            confetti.remove();

        }, 4000);

    }

}

/* =========================================
   ADD MONEY
========================================= */

async function submitAddMoney() {

    const amount =
    document.getElementById(
        "addAmount"
    ).value;

    const utr =
    document.getElementById(
        "utr"
    ).value;

    const screenshot =
    document.getElementById(
        "screenshot"
    ).files[0];

    if (!amount || !utr || !screenshot) {

        showToast(
            "Please fill all fields",
            "error"
        );

        return;

    }

    const token =
    getToken();

    if (!token) {

        showToast(
            "Please login first",
            "error"
        );

        return;

    }

    const formData =
    new FormData();

    formData.append(
        "amount",
        amount
    );

    formData.append(
        "utr_number",
        utr
    );

    formData.append(
        "payment_method",
        "UPI"
    );

    formData.append(
        "screenshot",
        screenshot
    );

    const btn =
    document.querySelector(
        ".wallet-submit-btn"
    );

    try {

        btn.disabled = true;

        btn.innerHTML = `

            <span class="loader"></span>
            Submitting...

        `;

        const response =
        await fetch(
            "/recharge/api/add-money/",
            {

                method: "POST",

                headers: {

                    Authorization:
                    `Bearer ${token}`

                },

                body: formData

            }
        );

        const data =
        await response.json();

        btn.disabled = false;

        btn.innerHTML =
        "💰 Submit Payment";

        if (response.ok) {

            showToast(
                data.message ||
                "Payment submitted"
            );

            document.getElementById(
                "addAmount"
            ).value = "";

            document.getElementById(
                "utr"
            ).value = "";

            document.getElementById(
                "screenshot"
            ).value = "";

            loadWallet();

        } else {

            showToast(
                data.message ||
                "Something went wrong",
                "error"
            );

        }

    } catch (error) {

        console.log(error);

        btn.disabled = false;

        btn.innerHTML =
        "💰 Submit Payment";

        showToast(
            "Server Error",
            "error"
        );

    }

}

/* =========================================
   COPY UPI
========================================= */

function copyUPI() {

    const upi =
    document.getElementById(
        "upiText"
    ).innerText;

    navigator.clipboard.writeText(upi);

    showToast(
        "UPI ID Copied"
    );

}

/* =========================================
   FLOATING LIVE ACTIVITY
========================================= */

const liveMessages = [

    "⚡ Recharge completed instantly",
    "🎁 Cashback credited to wallet",
    "💰 Wallet recharge now available",
    "🚀 Secure AI powered payments",
    "🔥 Fastest recharge experience"

];

let activityIndex = 0;

function rotateLiveActivity() {

    const activity =
    document.getElementById(
        "liveActivityText"
    );

    if (!activity) return;

    activity.innerText =
    liveMessages[activityIndex];

    activityIndex++;

    if (
        activityIndex >=
        liveMessages.length
    ) {

        activityIndex = 0;

    }

}

setInterval(
    rotateLiveActivity,
    3000
);

/* =========================================
   PAGE LOAD
========================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadWallet();

        loadProviders();

        loadCoupons();

        rotateLiveActivity();

    }
);