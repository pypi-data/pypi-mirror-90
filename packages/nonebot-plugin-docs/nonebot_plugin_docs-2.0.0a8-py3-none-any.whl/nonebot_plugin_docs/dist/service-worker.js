/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [
  {
    "url": "2.0.0a7/advanced/export-and-require.html",
    "revision": "f2eeffe4b77a645f521b45b94d062edb"
  },
  {
    "url": "2.0.0a7/advanced/index.html",
    "revision": "13acf04a40bf239b121c0b975b7c4c13"
  },
  {
    "url": "2.0.0a7/advanced/permission.html",
    "revision": "c948f4ac337b55fb0ad19d4465bee599"
  },
  {
    "url": "2.0.0a7/advanced/publish-plugin.html",
    "revision": "b082ccca0054f8eaf2488feb2998cbb3"
  },
  {
    "url": "2.0.0a7/advanced/runtime-hook.html",
    "revision": "c83acd43eb2319f11f24b85cd2399672"
  },
  {
    "url": "2.0.0a7/advanced/scheduler.html",
    "revision": "8325b9ce922a382573ec95d84e1db255"
  },
  {
    "url": "2.0.0a7/api/adapters/cqhttp.html",
    "revision": "d39a043296b8efea57c873c9a8150885"
  },
  {
    "url": "2.0.0a7/api/adapters/ding.html",
    "revision": "dd267923d5a9a88455018d6861b2e9b2"
  },
  {
    "url": "2.0.0a7/api/adapters/index.html",
    "revision": "08a9a75a216ac4f6bdafe28c29cae809"
  },
  {
    "url": "2.0.0a7/api/config.html",
    "revision": "6bd5c40f22d7d58aa67d22e81356154d"
  },
  {
    "url": "2.0.0a7/api/drivers/fastapi.html",
    "revision": "4ba12a30e569123fc22f7acdfd9f2d72"
  },
  {
    "url": "2.0.0a7/api/drivers/index.html",
    "revision": "09b19dd766f34a9444030e606387129f"
  },
  {
    "url": "2.0.0a7/api/exception.html",
    "revision": "e94288fe55163b0526ac5b22df6f7bb2"
  },
  {
    "url": "2.0.0a7/api/index.html",
    "revision": "84c66f0218b31dd1c1d9a7f5dd9c76c5"
  },
  {
    "url": "2.0.0a7/api/log.html",
    "revision": "9ca7409f65a8f8fa5de202bfa6416667"
  },
  {
    "url": "2.0.0a7/api/matcher.html",
    "revision": "4fc634dec5f8220ebcaf144c433c1b73"
  },
  {
    "url": "2.0.0a7/api/message.html",
    "revision": "d6a1cf08f5dd4f6d52c07bfff50d7dc6"
  },
  {
    "url": "2.0.0a7/api/nonebot.html",
    "revision": "15ffe36b75c2d5da6cdf1ffc7930db17"
  },
  {
    "url": "2.0.0a7/api/permission.html",
    "revision": "873c3e553c0438b4b3b4daa20edfaa0d"
  },
  {
    "url": "2.0.0a7/api/plugin.html",
    "revision": "f736f6975abfcd6730625bd20e9647f9"
  },
  {
    "url": "2.0.0a7/api/rule.html",
    "revision": "1d59d7a9a8cc1805e0a82da6e917c644"
  },
  {
    "url": "2.0.0a7/api/typing.html",
    "revision": "db56b46f2421f91e519c2973d157a7c8"
  },
  {
    "url": "2.0.0a7/api/utils.html",
    "revision": "b8abc71791cf49b5d3c3a23dfdc8fec9"
  },
  {
    "url": "2.0.0a7/guide/basic-configuration.html",
    "revision": "2e92be5b6f8201f0dbec1c02d4d76b9e"
  },
  {
    "url": "2.0.0a7/guide/creating-a-handler.html",
    "revision": "06d875000e95a03fcbb1fd956ae9198e"
  },
  {
    "url": "2.0.0a7/guide/creating-a-matcher.html",
    "revision": "0b9af7623a02e1fb24d7c852734e1ae9"
  },
  {
    "url": "2.0.0a7/guide/creating-a-plugin.html",
    "revision": "22969af1c7cfa0ae9af9a29b1c773872"
  },
  {
    "url": "2.0.0a7/guide/creating-a-project.html",
    "revision": "fd1a88abda81b4e0ceaf9b52bb27f6d3"
  },
  {
    "url": "2.0.0a7/guide/end-or-start.html",
    "revision": "638a51473b2743b7b75aac9e3224d875"
  },
  {
    "url": "2.0.0a7/guide/getting-started.html",
    "revision": "d33a8773bd6be7247d03efd46d49b895"
  },
  {
    "url": "2.0.0a7/guide/index.html",
    "revision": "5d233e6a6bb55b2ed246b06467d8f3df"
  },
  {
    "url": "2.0.0a7/guide/installation.html",
    "revision": "0cefff5247c8919994c8cc745029de39"
  },
  {
    "url": "2.0.0a7/guide/loading-a-plugin.html",
    "revision": "ce96b4f3799df96d6ed7d42efbb322f4"
  },
  {
    "url": "2.0.0a7/index.html",
    "revision": "21d87f41b4d5efe2785ac0e1e22d213d"
  },
  {
    "url": "404.html",
    "revision": "687f3a32533c32d021acb7d648016897"
  },
  {
    "url": "advanced/export-and-require.html",
    "revision": "b2679b10db999262cfbcf7d13bf61eaf"
  },
  {
    "url": "advanced/index.html",
    "revision": "1b8d6d8a23393303826d08b475f373b2"
  },
  {
    "url": "advanced/overloaded-handlers.html",
    "revision": "2d3cd45639a8a064e8ef4ac9c2116c2a"
  },
  {
    "url": "advanced/permission.html",
    "revision": "417fe699e6b46f5af76b6db6101f7539"
  },
  {
    "url": "advanced/publish-plugin.html",
    "revision": "d9e9204a159f5a0411de01891364af59"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "a7bfe771bd8a578ce012e39d6ebb5188"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "d8e4090c5276778fa61b4e009137ba5c"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "27d211f30a19dcdb3c3d171e72440877"
  },
  {
    "url": "api/adapters/ding.html",
    "revision": "833041a4593a253df9045395dae9ebdd"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "817d5735bb349f9d20f526e8eb5630bd"
  },
  {
    "url": "api/config.html",
    "revision": "b319b7ed94c3397a18b7d83d9b04a4fb"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "ce150de6c32fb46c99a53aab97d16c1a"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "6f7b0a636e740c45b41f928decfaf0df"
  },
  {
    "url": "api/exception.html",
    "revision": "ffa399696868b1ef104661466197b178"
  },
  {
    "url": "api/index.html",
    "revision": "bbb91fea58070df1e3beae7a4c41ccc0"
  },
  {
    "url": "api/log.html",
    "revision": "326b582a9284373d9771d303f2d72ce3"
  },
  {
    "url": "api/matcher.html",
    "revision": "a810aed36b45a3877f0919c9f828ac93"
  },
  {
    "url": "api/message.html",
    "revision": "4ae876ba735632c10ca0e478b05a82bd"
  },
  {
    "url": "api/nonebot.html",
    "revision": "77c1d213ab106aa2c408f7d2f1400f43"
  },
  {
    "url": "api/permission.html",
    "revision": "a70e8e3be7a3a7919d962362df323d22"
  },
  {
    "url": "api/plugin.html",
    "revision": "b4151a9bc390f757d17b9238033a28a5"
  },
  {
    "url": "api/rule.html",
    "revision": "4dc3c9d79f33c6c5026a377b62de86a2"
  },
  {
    "url": "api/typing.html",
    "revision": "6050cfa3f7262def10018ec24afdec80"
  },
  {
    "url": "api/utils.html",
    "revision": "1943747327bf4198797eb8a88b4bda39"
  },
  {
    "url": "assets/css/0.styles.49c81ce6.css",
    "revision": "16daa387e964eb70cfc34b4c8cbabd5c"
  },
  {
    "url": "assets/img/search.237d6f6a.svg",
    "revision": "237d6f6a3fe211d00a61e871a263e9fe"
  },
  {
    "url": "assets/img/search.83621669.svg",
    "revision": "83621669651b9a3d4bf64d1a670ad856"
  },
  {
    "url": "assets/js/10.28c1c8c5.js",
    "revision": "840072ff191b8b2516fba79dbe6b8236"
  },
  {
    "url": "assets/js/100.0aa2b9c9.js",
    "revision": "778a20b83d857a906fd00a55045ab1c7"
  },
  {
    "url": "assets/js/101.ba344a23.js",
    "revision": "d6103d86dc75a6842df06cb97908b677"
  },
  {
    "url": "assets/js/102.108a3ef7.js",
    "revision": "9a1c40c0b821a6afe1ea15aeee554504"
  },
  {
    "url": "assets/js/103.faeaccd7.js",
    "revision": "42f473780a990d12b59c356c28c171d3"
  },
  {
    "url": "assets/js/104.e855e28f.js",
    "revision": "0fb7bc0d02e127656807a0f5df6d3106"
  },
  {
    "url": "assets/js/105.5fa4f2d5.js",
    "revision": "15b40638687ba9b0bad1be66e04fb1a9"
  },
  {
    "url": "assets/js/106.e2d52cf9.js",
    "revision": "fd574600e4d39419f8befcc78f386ec6"
  },
  {
    "url": "assets/js/107.53a79303.js",
    "revision": "089253c390fb1540591a92013fd91473"
  },
  {
    "url": "assets/js/108.9b6cbd2b.js",
    "revision": "e67578c8319e16d361c0e92b44eb1f0b"
  },
  {
    "url": "assets/js/109.048007d8.js",
    "revision": "618e32177085ff35fd77a2a9bd527b0c"
  },
  {
    "url": "assets/js/11.23246db0.js",
    "revision": "9b74e75eea9ae2049a02db798d08f26d"
  },
  {
    "url": "assets/js/110.55ae0f89.js",
    "revision": "6e039eb152499f29ea27dcd8274a7e84"
  },
  {
    "url": "assets/js/111.71469f9f.js",
    "revision": "b1f7f85bfd92c2ec3c8188aab61ba3d0"
  },
  {
    "url": "assets/js/112.e36b2662.js",
    "revision": "850d258e87a02c633ec03e6570a6a7bd"
  },
  {
    "url": "assets/js/113.494cefad.js",
    "revision": "4bc5b14c6a4bf456cd7115a30c65ad04"
  },
  {
    "url": "assets/js/114.84070937.js",
    "revision": "23bbf0b8fd74e9d547f211ce028d3601"
  },
  {
    "url": "assets/js/115.b33db9e9.js",
    "revision": "5bd4990f3a25d6bc18c60b59c50e4662"
  },
  {
    "url": "assets/js/116.836b6017.js",
    "revision": "e9710379090aef2cf126da09312978e3"
  },
  {
    "url": "assets/js/117.1f3fd674.js",
    "revision": "8baeb7bb80fe3e3f5dc00a9017d405b8"
  },
  {
    "url": "assets/js/118.91f9645f.js",
    "revision": "ffb9d0b715dfc81f0979b066d85a0a01"
  },
  {
    "url": "assets/js/119.34ffba23.js",
    "revision": "fda062dd2a4773c9231a17097733d76c"
  },
  {
    "url": "assets/js/12.272c6820.js",
    "revision": "a71b251392e4ae8f1fe2813ecceb8b88"
  },
  {
    "url": "assets/js/13.b09abc6d.js",
    "revision": "2a7894cf81be8f243955471dcc6222a4"
  },
  {
    "url": "assets/js/14.3b7d1b68.js",
    "revision": "659ea06188f0514d9fbadb894f3db694"
  },
  {
    "url": "assets/js/15.bf0eddf5.js",
    "revision": "df99b1d3019b1d7cfe0be338dc00a2c1"
  },
  {
    "url": "assets/js/16.2585a0f8.js",
    "revision": "786660c791530788b6978145c5156ab2"
  },
  {
    "url": "assets/js/17.49ba0f55.js",
    "revision": "2e2599c13a2cb684dc114610f1c13a6b"
  },
  {
    "url": "assets/js/18.c8dd93fb.js",
    "revision": "de183ac0a3a7a37a71b1b6e9af29c4c4"
  },
  {
    "url": "assets/js/19.85f95c64.js",
    "revision": "5ee20fb4e85b8e4bf0c741c6138b61d8"
  },
  {
    "url": "assets/js/2.c84f7eb9.js",
    "revision": "69bb4fc50d5d4831886aa38cb858ad97"
  },
  {
    "url": "assets/js/20.7e10e37d.js",
    "revision": "85245eeca1bca187ee381f7cac6b903b"
  },
  {
    "url": "assets/js/21.45cb5d06.js",
    "revision": "1711246a7f6b6cd6f18f7e6830fd2954"
  },
  {
    "url": "assets/js/22.303d9965.js",
    "revision": "56a8a768c72d50ca8e4407c479913897"
  },
  {
    "url": "assets/js/23.8481bf65.js",
    "revision": "ed5d88719c298b86db622b27a5b2e14e"
  },
  {
    "url": "assets/js/24.ebd72834.js",
    "revision": "43b49c55a78bfd9fd972ff27290c60bc"
  },
  {
    "url": "assets/js/25.0682441d.js",
    "revision": "fec7aa55a02fdcd8b7367844fa8a9717"
  },
  {
    "url": "assets/js/26.92eb06d9.js",
    "revision": "04a9df6c7482d7e6235b49c743856f80"
  },
  {
    "url": "assets/js/27.01082146.js",
    "revision": "d97b94453de98ce30b5f130aa85f6b8e"
  },
  {
    "url": "assets/js/28.e960975c.js",
    "revision": "c3227657205b50d251673a090b3c1834"
  },
  {
    "url": "assets/js/29.7a94e670.js",
    "revision": "955ea3daf7f28509e0513e80b19242bc"
  },
  {
    "url": "assets/js/3.87435b6a.js",
    "revision": "4d71ee736540cb05cb380b36643921cc"
  },
  {
    "url": "assets/js/30.486615ee.js",
    "revision": "37c305207221b9d52ce4e2c5617f78ed"
  },
  {
    "url": "assets/js/31.c319ab9f.js",
    "revision": "1002edff36bda4e5657e521f56eff936"
  },
  {
    "url": "assets/js/32.a9811cfc.js",
    "revision": "07fe2195d50b27d499aecaa890c89f6e"
  },
  {
    "url": "assets/js/33.7bb3c874.js",
    "revision": "d0b5f97695a1849aa16818696778d650"
  },
  {
    "url": "assets/js/34.27202e66.js",
    "revision": "1040016006e3ff67819660abba666ed7"
  },
  {
    "url": "assets/js/35.7f2205ba.js",
    "revision": "cfabea12a7c0d3c6d56c336d8774ad40"
  },
  {
    "url": "assets/js/36.990546b5.js",
    "revision": "d68def4aae99716f5e2580235e5bac52"
  },
  {
    "url": "assets/js/37.b45f9312.js",
    "revision": "3c33dccd3ed1e5533eae2bb080653e84"
  },
  {
    "url": "assets/js/38.b054f867.js",
    "revision": "0e365b1a606052dae0d73e77385d38ed"
  },
  {
    "url": "assets/js/39.eae4a822.js",
    "revision": "0d0dfca03c6bc4638d1cfd0fa3119a85"
  },
  {
    "url": "assets/js/4.8df46d24.js",
    "revision": "71fee54f67a404aca2a106ab41e63e5e"
  },
  {
    "url": "assets/js/40.2e55c49a.js",
    "revision": "914bca3ba4a91eb9f74f313043f0badf"
  },
  {
    "url": "assets/js/41.dcc2aabb.js",
    "revision": "df400969eeaea2c3114f8705b19c367a"
  },
  {
    "url": "assets/js/42.e1536973.js",
    "revision": "1ef9ca425234140a05af1998bf39393c"
  },
  {
    "url": "assets/js/43.227fd122.js",
    "revision": "4ceafbd736de3eab7bb3b378c87349f1"
  },
  {
    "url": "assets/js/44.5182f3a3.js",
    "revision": "1bb54d9860d247a87325e73411f1cb39"
  },
  {
    "url": "assets/js/45.283966a1.js",
    "revision": "2635e600fc0a6db890f0e58a9ddda873"
  },
  {
    "url": "assets/js/46.31ebaa79.js",
    "revision": "e093f80866882320b56a026559bbdfb3"
  },
  {
    "url": "assets/js/47.ec517c1f.js",
    "revision": "5163b9a41d06a04ff12133984a25dcb7"
  },
  {
    "url": "assets/js/48.6a4f68c5.js",
    "revision": "41b2c4f40c6e6bfd9ca5e16e09592328"
  },
  {
    "url": "assets/js/49.78a153f2.js",
    "revision": "dd48adfb241e36a6f1fe9b5d04c966cd"
  },
  {
    "url": "assets/js/5.1299c054.js",
    "revision": "077af6c44ce4d6790e08acadf1b55cf6"
  },
  {
    "url": "assets/js/50.485190f1.js",
    "revision": "60dddb9c4a8205163b55b83e795853ad"
  },
  {
    "url": "assets/js/51.f8a4f722.js",
    "revision": "4a4f2bb1d742f66c6683420b1a9d6c08"
  },
  {
    "url": "assets/js/52.7d61afe8.js",
    "revision": "19ca86b4313a5eabf4d5ca98679e9335"
  },
  {
    "url": "assets/js/53.fc07a827.js",
    "revision": "735eedf5d56aac5559d209e0ce965d89"
  },
  {
    "url": "assets/js/54.407d4cc0.js",
    "revision": "0ef8fae20117997cb7e8d63c73b7febf"
  },
  {
    "url": "assets/js/55.508d6680.js",
    "revision": "b0da76cb4c1c70e9e1575c4af2f04afd"
  },
  {
    "url": "assets/js/56.dba215d4.js",
    "revision": "7ead21e040a1383880275f7d5b66779e"
  },
  {
    "url": "assets/js/57.154d4c7f.js",
    "revision": "ea0e04dfef4b0d86e50aa9dcb8a0c139"
  },
  {
    "url": "assets/js/58.9aef2cfe.js",
    "revision": "bb3b799b43eb009431a23ccaef97b862"
  },
  {
    "url": "assets/js/59.f2c8780b.js",
    "revision": "a9ae0161ff2ca218f790b0a5507de5e5"
  },
  {
    "url": "assets/js/6.b71be673.js",
    "revision": "11228413bf4ceab71d2ec31eac9d9a0b"
  },
  {
    "url": "assets/js/60.d16d9bc3.js",
    "revision": "d99eddad25089fa7066bef22b969ab3d"
  },
  {
    "url": "assets/js/61.04af0980.js",
    "revision": "7d64b5e10c1da7be5c20bbf5aa2da2fd"
  },
  {
    "url": "assets/js/62.54e06c82.js",
    "revision": "f295d8f9775ed951a977cd2b4b04feed"
  },
  {
    "url": "assets/js/63.2e486b06.js",
    "revision": "f1b4c8b7423abf468b1dabec8817b085"
  },
  {
    "url": "assets/js/64.b0a3df0f.js",
    "revision": "f7ef58b5454f4ee28d76fd87af1aaf91"
  },
  {
    "url": "assets/js/65.a4a85801.js",
    "revision": "ebf3b883613504591fc999ae179263eb"
  },
  {
    "url": "assets/js/66.19ce598f.js",
    "revision": "f65b3b2bc689a8377cd4628bc39ddb5c"
  },
  {
    "url": "assets/js/67.364fb85b.js",
    "revision": "5208cdc3c133fa73130facd48aaaa013"
  },
  {
    "url": "assets/js/68.518a2cae.js",
    "revision": "a408ffc7f3dfe873ee92b10baabec613"
  },
  {
    "url": "assets/js/69.73a891a0.js",
    "revision": "f80a14fe0f0477642d66ec4a19d8067f"
  },
  {
    "url": "assets/js/7.28680298.js",
    "revision": "09b27a60abea1d0313f2fddec2b8600f"
  },
  {
    "url": "assets/js/70.d21a9c19.js",
    "revision": "dd3c7aa27978e7642ff8ff0c7115551b"
  },
  {
    "url": "assets/js/71.cbf3b3cc.js",
    "revision": "7a2cb28c226f7b0777f1b5b4c6e1fec3"
  },
  {
    "url": "assets/js/72.ead1ddb7.js",
    "revision": "6551a7e031d14adb6f7bc476df7ad113"
  },
  {
    "url": "assets/js/73.26bd1bfd.js",
    "revision": "7418331d71a4eea09be14f9e7e04144b"
  },
  {
    "url": "assets/js/74.ffac3b0a.js",
    "revision": "b20cc63093d4bbe2d22642c3aafa5aa2"
  },
  {
    "url": "assets/js/75.33f4acac.js",
    "revision": "e7a69c518e36fe841bd9f9fef15b4b69"
  },
  {
    "url": "assets/js/76.0aed12bb.js",
    "revision": "cf7e93a2519a8c27de0e5ce8905f595c"
  },
  {
    "url": "assets/js/77.b5f70f4d.js",
    "revision": "49f4d8b0b8c5f29eb4878983c98ca519"
  },
  {
    "url": "assets/js/78.897f5fb4.js",
    "revision": "bbb3ddbc15590344c916846dc0293755"
  },
  {
    "url": "assets/js/79.29e2b619.js",
    "revision": "96e2039e286f7ed82f612cb2682012cf"
  },
  {
    "url": "assets/js/8.6151909e.js",
    "revision": "36067ca3f868a72e6f3ae43c93068b2a"
  },
  {
    "url": "assets/js/80.fff6a2fd.js",
    "revision": "76cfa742ed08498cb6be80f246c394f3"
  },
  {
    "url": "assets/js/81.c673fcb9.js",
    "revision": "ad427706a86f6ec44ba45a766cd5452f"
  },
  {
    "url": "assets/js/82.abce9fae.js",
    "revision": "57c707c7929d518fdf241387a6f3d232"
  },
  {
    "url": "assets/js/83.bdb2a65e.js",
    "revision": "44afd6d62ce7b6ddba10a2f7ecbd0a0d"
  },
  {
    "url": "assets/js/84.2ba31590.js",
    "revision": "a097e4ac49151db551ac4c1a67c68136"
  },
  {
    "url": "assets/js/85.ce4858f3.js",
    "revision": "c7419b7a8ae79f081333b05fb22a3f5b"
  },
  {
    "url": "assets/js/86.0cfe6d73.js",
    "revision": "fedb1ce310203b5cf7e85a49e7268b0b"
  },
  {
    "url": "assets/js/87.3a3966aa.js",
    "revision": "d99e32ea44df925efaeb5e38397224b2"
  },
  {
    "url": "assets/js/88.7df4f597.js",
    "revision": "1c9a25d0e98c07ea69aa9488da8e0924"
  },
  {
    "url": "assets/js/89.9b3bdeee.js",
    "revision": "7e9ac126d2d2604cd3ecee13a94becb4"
  },
  {
    "url": "assets/js/9.a3422899.js",
    "revision": "1778058aa634fb91f13f373b79370972"
  },
  {
    "url": "assets/js/90.e9d0f1f1.js",
    "revision": "4b870bc29d4649c7353b7b432316c13d"
  },
  {
    "url": "assets/js/91.f7f5aa29.js",
    "revision": "7fb1d579881368e2a596e0c0d55b7c8b"
  },
  {
    "url": "assets/js/92.bdb0b593.js",
    "revision": "be2a1a9cc09f01fef1e84748d126dec9"
  },
  {
    "url": "assets/js/93.31d223c1.js",
    "revision": "d286ec418c7d545fea29e6882c7c6863"
  },
  {
    "url": "assets/js/94.6f75de56.js",
    "revision": "00ede32cd6142a1196f9c2ca2320a30b"
  },
  {
    "url": "assets/js/95.3635ce13.js",
    "revision": "d097c8b6be2314c94dc2d107009a0fa8"
  },
  {
    "url": "assets/js/96.5355fdcd.js",
    "revision": "51b0ba8787c43f04e2d9fa7d49a26acd"
  },
  {
    "url": "assets/js/97.ac7f21fa.js",
    "revision": "9a75f711369a357e850a8de97e3a3cc3"
  },
  {
    "url": "assets/js/98.567d92ad.js",
    "revision": "5fcf89db1ef7525fe66e31a36f10b84b"
  },
  {
    "url": "assets/js/99.9cc2aeff.js",
    "revision": "47cade6d8543a23238b42e0e165a926b"
  },
  {
    "url": "assets/js/app.7db4af6f.js",
    "revision": "22a1990b238caed400d686838f54b072"
  },
  {
    "url": "changelog.html",
    "revision": "1a98121ee33c18f9d6fc61fa19bcd570"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "aa86a33a53118bbd5fde01ded7581725"
  },
  {
    "url": "guide/cqhttp-guide.html",
    "revision": "e82b4d40fb2181cb4586b45e676a2f51"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "e4533261d6a0329c498564f1a61b16c7"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "64b945edb50b3a5adc00274d1343db97"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "c08c7e9d9ccfdaca6ea1785a64c91a1b"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "73a7e7463d0e79fe03d613c119851566"
  },
  {
    "url": "guide/ding-guide.html",
    "revision": "896dd5e431b88cb0389f8631e1a4d107"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "0fa31a8020a63f6154e91e28ebc20f03"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "0ad1863f6dc92cc06aea4d6f3a0d4f20"
  },
  {
    "url": "guide/index.html",
    "revision": "54b9560192ab0517a2a102dd49a69da3"
  },
  {
    "url": "guide/installation.html",
    "revision": "8ddb8bd286edd6297126525a13c8d076"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "539c8917a9813ef7f4a424e6b207a632"
  },
  {
    "url": "icons/android-chrome-192x192.png",
    "revision": "36b48f1887823be77c6a7656435e3e07"
  },
  {
    "url": "icons/android-chrome-384x384.png",
    "revision": "e0dc7c6250bd5072e055287fc621290b"
  },
  {
    "url": "icons/apple-touch-icon-180x180.png",
    "revision": "b8d652dd0e29786cc95c37f8ddc238de"
  },
  {
    "url": "icons/favicon-16x16.png",
    "revision": "e6c309ee1ea59d3fb1ee0582c1a7f78d"
  },
  {
    "url": "icons/favicon-32x32.png",
    "revision": "d42193f7a38ef14edb19feef8e055edc"
  },
  {
    "url": "icons/mstile-150x150.png",
    "revision": "a76847a12740d7066f602a3e627ec8c3"
  },
  {
    "url": "icons/safari-pinned-tab.svg",
    "revision": "18f1a1363394632fa5fabf95875459ab"
  },
  {
    "url": "index.html",
    "revision": "f5982d653970d1e2eaed53b3580e9a13"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/export-and-require.html",
    "revision": "fa4a094e270f0cabbf79b8758bd47f09"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "d6a61ab7fd6b1d3389562824771d6b00"
  },
  {
    "url": "next/advanced/overloaded-handlers.html",
    "revision": "b389b9459bbf2d0829d7ef74efbae9c3"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "20955b8499d95d1adc1e73c2fcbc05c2"
  },
  {
    "url": "next/advanced/publish-plugin.html",
    "revision": "e4e38fe9fc63055f58207acf2ce0925d"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "0534585916751ed86b9c7515a34f5fee"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "94f9ab5bc060abc897630ee878089f45"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "c3bc6878a66ea392d5a8a5605f3d4d72"
  },
  {
    "url": "next/api/adapters/ding.html",
    "revision": "de1c123e7b2138eedc9e2d7769c5ad94"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "15938a683f5df2ef72771bf89a3c5c4d"
  },
  {
    "url": "next/api/config.html",
    "revision": "fcb7c09d6167660a884a8d11a12127e5"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "02b0aea93bdf3e911c84a3130fa1fb56"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "5574422770d71caeee9a0f9609c56626"
  },
  {
    "url": "next/api/exception.html",
    "revision": "e3e39628237e253894b8659216a8845c"
  },
  {
    "url": "next/api/index.html",
    "revision": "3dfbaec352c54216468dc70f3e5338a3"
  },
  {
    "url": "next/api/log.html",
    "revision": "69f646569fe4d664a5a4be097a91a7f8"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "8bf524a53baaf2bfab7f2a6c8fb5d3f1"
  },
  {
    "url": "next/api/message.html",
    "revision": "3eff49e40dea6ca31181abb1e7c85115"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "85c45470d5bf3bf51f6f608697a3d9a0"
  },
  {
    "url": "next/api/permission.html",
    "revision": "2403896e12d74bcf021a3a200e688b04"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "0b05803eef79461e7af94f4839eb7cc8"
  },
  {
    "url": "next/api/rule.html",
    "revision": "270f822c9e93b8e1a025173945f858e5"
  },
  {
    "url": "next/api/typing.html",
    "revision": "d3e453d17cae8636fb0afaa5454941d0"
  },
  {
    "url": "next/api/utils.html",
    "revision": "3bcb7e90065dd78bc9b776462e9f0d87"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "8508f418bf96e5700cdc50335c1bc2d5"
  },
  {
    "url": "next/guide/cqhttp-guide.html",
    "revision": "0950d8c6caa0afd8b209133147d8b66e"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "78f1ce767b48fee49040cea6f38defa5"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "ba128e5ddf60a585a6c0d82db76bdab1"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "4f2beac02e6572016f90dba6e468992f"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "a3fba99f4d42443b2ed860211cf24800"
  },
  {
    "url": "next/guide/ding-guide.html",
    "revision": "ede9885395eab574bcbee18b952a6240"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "2d242a5363c866e4cb36fe3d93ffe6b6"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "22df36e1360cfd17e41c4bde38a2f0c5"
  },
  {
    "url": "next/guide/index.html",
    "revision": "6a52e8956d21571796bb415231390ad1"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "6dc78cfc125f7e67a4690d0b387530b5"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "170872d908ff6db7aadb397b61eb0d8d"
  },
  {
    "url": "next/index.html",
    "revision": "0c1c0d07046fb8338e60c4d486fa7aca"
  },
  {
    "url": "plugin-store.html",
    "revision": "318d195ca6266f1fdda2af92af45bf39"
  }
].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
addEventListener('message', event => {
  const replyPort = event.ports[0]
  const message = event.data
  if (replyPort && message && message.type === 'skip-waiting') {
    event.waitUntil(
      self.skipWaiting().then(
        () => replyPort.postMessage({ error: null }),
        error => replyPort.postMessage({ error })
      )
    )
  }
})
