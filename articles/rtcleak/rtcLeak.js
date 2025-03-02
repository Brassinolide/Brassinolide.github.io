function rtcLeak(stun = "stun:stun.l.google.com:19302") {
    return new Promise((resolve, reject) => {
        const myPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection || window.msRTCPeerConnection;
        const pc = new myPeerConnection({ iceServers: [{ urls: stun }] });
        pc.createDataChannel("");
        pc.onicecandidate = (event) => {
            if (event && event.candidate && event.candidate.candidate) {
                const ipRegex = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/;
                const ipMatch = event.candidate.candidate.match(ipRegex);

                if (ipMatch) {
                    pc.close();
                    resolve(ipMatch[1]);
                }
            }
        };
        pc.createOffer()
            .then((offer) => pc.setLocalDescription(offer))
            .catch((error) => {
                reject(error);
            });
    });
}

rtcLeak()
    .then((ip) => {
        alert(ip)
    })
    .catch((error) => {
        console.error(error);
    });
