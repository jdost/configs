pragma Singleton
import QtQuick
import Quickshell
import Quickshell.Services.Mpris

Singleton {
    id: mprisTracker

    property MprisPlayer currentPlayer: null
    property var playerStatuses

    function updatePlayerStates() {
        var playing = [];
        var lastPlayingTime = -1;
        var lastPlaying;
        const current = new Date().valueOf();
        if (playerStatuses === undefined)
            playerStatuses = {};

        var toDelete = Object.keys(playerStatuses);
        for (const i in Mpris.players.values) {
            const player = Mpris.players.values[i];
            if (playerStatuses[player.identity] && playerStatuses[player.identity].ref === null)
                continue;

            const toDeleteIndex = toDelete.indexOf(player.identity);
            if (toDeleteIndex !== -1) {
                toDelete.splice(toDeleteIndex, 1);
            }

            if (playerStatuses[player.identity] === undefined || playerStatuses[player.identity].ref !== player) {
                playerStatuses[player.identity] = {
                    "name": player.identity,
                    "ref": player,
                    "playingSince": player.isPlaying ? current : -1,
                    "lastPlaying": player.isPlaying ? current : -1,
                    "lastStatus": player.playbackState
                };
                player.onPlaybackStateChanged.connect(updatePlayerStates);
            } else {
                if (player.isPlaying) {
                    playerStatuses[player.identity].lastPlaying = current;
                } else if (player.playbackState != playerStatuses[player.identity].lastStatus) {
                    if (player.isPlaying)
                        playerStatuses[player.identity].playingSince = current;

                    playerStatuses[player.identity].lastStatus = player.playbackState;
                }
            }
        }

        for (const i in toDelete) {
            console.log(`Deleting ${toDelete[i]}...`);
            delete playerStatuses[toDelete[i]];
        }
        var active = null;
        for (const k in playerStatuses) {
            const player = playerStatuses[k];
            if (player.lastStatus === MprisPlaybackState.Playing) {
                if (active === null)
                    active = player;
                else if (active.lastPlaying < player.lastPlaying)
                    active = player;
            } else if (active === null)
                active = player;
            else if (active.lastStatus === MprisPlaybackState.Playing)
                continue;
            else if (active.lastPlaying < player.lastPlaying)
                active = player;
        }
        if (!active)
            console.log("No active player");
        else
            console.log(`Active player: ${active.name}`);
        if (active)
            currentPlayer = active.ref;
    }

    Component.onCompleted: {
        updatePlayerStates();
    }

    Connections {
        function onValuesChanged() {
            updatePlayerStates();
        }

        target: Mpris.players
    }
}
