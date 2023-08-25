"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var THREE = require("https://cdn.jsdelivr.net/npm/three@0.130.0/build/three.module.js");
var OrbitControls_js_1 = require("https://cdn.jsdelivr.net/npm/three@0.130.0/examples/jsm/controls/OrbitControls.js");
var OBJLoader_js_1 = require("https://cdn.jsdelivr.net/npm/three@0.130.0/examples/jsm/loaders/OBJLoader.js");
var MTLLoader_js_1 = require("https://cdn.jsdelivr.net/npm/three@0.130.0/examples/jsm/loaders/MTLLoader.js");
var stats_module_js_1 = require("https://cdn.jsdelivr.net/npm/three@0.130.0/examples/jsm/libs/stats.module.js");
var scene = new THREE.Scene();
scene.add(new THREE.AxesHelper(5));
var light = new THREE.PointLight(0xffffff, 1000);
light.position.set(2.5, 7.5, 15);
scene.add(light);
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 3;
var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
var controls = new OrbitControls_js_1.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
var mtlLoader = new MTLLoader_js_1.MTLLoader();
mtlLoader.load('models/monkey.mtl', function (materials) {
    materials.preload();
    console.log(materials);
    var objLoader = new OBJLoader_js_1.OBJLoader();
    objLoader.setMaterials(materials);
    objLoader.load('models/monkey.obj', function (object) {
        scene.add(object);
    }, function (xhr) {
        console.log((xhr.loaded / xhr.total) * 100 + '% loaded');
    }, function (error) {
        console.log('An error happened');
    });
}, function (xhr) {
    console.log((xhr.loaded / xhr.total) * 100 + '% loaded');
}, function (error) {
    console.log('An error happened');
});
window.addEventListener('resize', onWindowResize, false);
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    render();
}
var stats = new stats_module_js_1.default();
document.body.appendChild(stats.dom);
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    render();
    stats.update();
}
function render() {
    renderer.render(scene, camera);
}
animate();
