import qs
import qs.Popups
import qs.Services

Icon {
    readonly property var icons: {
        "spotify": ["󰓇", U.rgb(30, 215, 96)],
        "Spotifyd": ["󰓇", U.rgb(30, 215, 96)],
        "firefox": ["󰈹", U.rgb(230, 96, 0)],
        "Mozilla firefox": ["󰈹", U.rgb(230, 96, 0)],
        "chromium": ["", U.rgb(0, 136, 247)],
        "qutebrowser": ["󰖟", U.rgb(166, 223, 255)],
        "mpv": ["󰐌", U.rgb(200, 100, 255)],
        "DEFAULT": ["󰝚", U.rgb(255, 255, 255)]
    }

    function onClick() {
        popup.toggle();
    }

    icon: {
        if (!MprisTracker.currentPlayer)
            return icons["DEFAULT"][0];

        if (icons[MprisTracker.currentPlayer.identity] === undefined)
            return icons["DEFAULT"][0];

        return icons[MprisTracker.currentPlayer.identity][0];
    }
    iconColor: {
        if (!MprisTracker.currentPlayer)
            return U.rgb(153, 153, 153);

        if (!MprisTracker.currentPlayer.isPlaying)
            return U.rgb(153, 153, 153);

        if (icons[MprisTracker.currentPlayer.identity] === undefined)
            return icons["DEFAULT"][1];

        return icons[MprisTracker.currentPlayer.identity][1];
    }
    module: "mpris"
    size: Config.em(1.4)
    tooltip: {
        if (popup.shown)
            return "";

        return MprisTracker.currentPlayer ? MprisTracker.currentPlayer.identity : "Nothing";
    }
    topPadding: Config.em(0.05)
    onClicked: function() {
        if (!MprisTracker.currentPlayer && !popup.shown)
            return ;

        popup.toggle();
    }

    MprisPopup {
        id: popup

        player: MprisTracker.currentPlayer
    }

}
