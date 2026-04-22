pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Services.Pipewire

Singleton {
    id: volumeTracker

    PwObjectTracker {
        objects: [
            Pipewire.defaultAudioSink,
            Pipewire.defaultAudioSource,
        ]
	}

    property PwNode output: (Pipewire.defaultAudioSink && Pipewire.defaultAudioSink.isSink) ? Pipewire.defaultAudioSink : null
    property PwNode input: (Pipewire.defaultAudioSource && !Pipewire.defaultAudioSource.isSink) ? Pipewire.defaultAudioSource : null

    property bool outputIsMuted: (output && output.audio) ? output.audio.muted : true
    property real outputVolume: (output && output.audio) ? output.audio.volume : 0.0
    property bool inputIsMuted: (input && input.audio) ? input.audio.muted : true
    property real inputVolume: (input && input.audio) ? input.audio.volume : 0.0
}
