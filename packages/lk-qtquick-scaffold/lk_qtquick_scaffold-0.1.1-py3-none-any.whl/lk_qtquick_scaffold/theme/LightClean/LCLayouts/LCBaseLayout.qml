/*
    设计思想:


 */
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import "../LCBackground"
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/palette.js" as LCPalette

LCRectBg {
    id: root
    implicitWidth: LCDimension.WinWidth
    implicitHeight: LCDimension.WinHeight
    clip: true
    layer.enabled: p_clipRadius
    layer.effect: _clipRadiusMask

    p_color: LCPalette.Transparent

    property real p_availWidth: 0
    property real p_availHeight: 0
    property bool p_clipRadius: false
    property real p_spacing: LCDimension.HSpacingM
    property real p_hspacing: 0
    property real p_vspacing: 0

    function _adjustChildrenMargins() {
        for (let i in root.children) {
            const child = root.children[i]
            if (child.anchors.leftMargin == 0) {
                child.anchors.leftMargin = p_hspacing
            }
            if (child.anchors.rightMargin == 0) {
                child.anchors.rightMargin = p_hspacing
            }
            if (child.anchors.topMargin == 0) {
                child.anchors.topMargin = p_vspacing
            }
            if (child.anchors.bottomMargin == 0) {
                child.anchors.bottomMargin = p_vspacing
            }
        }
    }

    Component {
        id: _clipRadiusMask
        OpacityMask {
            maskSource: Rectangle {
                width: root.width
                height: root.height
                radius: root.radius
            }
        }
    }

    Component.onCompleted: {
        if (p_hspacing == 0) {
            p_hspacing = p_spacing
        }
        if (p_vspacing == 0) {
            p_vspacing = p_spacing
        }

        _adjustChildrenMargins()
    }
}

