import { Boot } from './scenes/Boot';
import { Preloader } from './scenes/Preloader';
import { Viewport } from './scenes/Viewport';
import { AUTO, Game } from 'phaser';

// Find out more information about the Game Config at:
// https://docs.phaser.io/api-documentation/typedef/types-core#gameconfig
const config = {
    /*
    type: AUTO,
    width: 1024,
    height: 768,
    parent: 'game-container',
    backgroundColor: '#028af8',
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },
    */
    type: Phaser.WEBGL,
    parent: 'game-container',
    pixelArt: true,
    backgroundColor: '#320822',
    disableContextMenu: true,
    scale:
    {
        mode: Phaser.Scale.NONE,
        //autoCenter: Phaser.Scale.CENTER_BOTH,
        width: 256,
        height: 128,
        zoom: 3
    },
    disablePreFX: true,
    disablePostFX: true,
    scene: [
        Boot,
        Preloader,
        Viewport
    ]
};

const StartGame = (parent) => {

    return new Game({ ...config, parent });

}

export default StartGame;
