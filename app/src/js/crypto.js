var polyfaucetABI = []



////////////////////////////////////////////////////////////////////////////////
// THIS PART IS DOPE AS SHIIIIIT      🌳🌳🌳🌳🌳🌳🌳🌳                       //
////////////////////////////////////////////////////////////////////////////////
// WHITELIST Merkle Tree
// var addresses = {{ addresses_list | tojson | safe}};
// Hash addresses to get the leaves
// var leaves = addresses.map(addr => keccak256(addr));
// Create tree
// var merkleTree = new MerkleTree(leaves, keccak256, { sortPairs: true })
// var rootHash = merkleTree.getRoot().toString('hex')
// console.log("rootHash: " + rootHash);
////////////////////////////////////////////////////////////////////////////////

const provider = new ethers.providers.Web3Provider(window.ethereum, "any");

// switch to Polygon
let web3 = window.ethereum;
web3
  .request({
    method: "wallet_switchEthereumChain",
    params: [{ chainId: "0x89" }]
  })
  .catch(() => { });

async function main() {


  // only works if on mainnet
  async function reverseResolveENS(address) {
    return address;
    console.log("reverseResolveENS: " + address);
    console.log(typeof address);
    // if address doesnt start with 0x, return 
    if (!address.startsWith("0x")) {
      return;
    }
    var name = await provider.lookupAddress(address);
    console.log("Resolved ENS name: " + name);
    return name;
  }


  // get all .ens-replace elements and replace them with the ens name if it exists
  var ens = document.getElementsByClassName('ens-replace');

  async function updateAddresses() {
    for (var i = 0; i < ens.length; i++) {
      // get child with class 'ens-replace-address'
      var address = ens[i].getElementsByClassName('ens-replace-address')[0];
      var name = await reverseResolveENS(address.innerHTML);
      if (name) {
        address.innerHTML = `<a href="https://app.ens.domains/name/"` + address.innerHTML + `" target="_blank" class="bold">` + name + `</a>`;

        //const avatar = await provider.getAvatar(name);
        //// if avatar is not null
        //if (avatar) {
        //  // get child with class 'ens-replace-avatar'
        //  var avatar_element = ens[i].getElementsByClassName('ens-replace-image')[0];
        //image.innerHTML = `<img src="` + avatar + `" alt="` + name + `" />`;
        //}
      }
    }
  }
  updateAddresses();
}
// main();


async function login() {
  // Prompt user for account connections
  await provider.send("eth_requestAccounts", []);
  const signer = provider.getSigner();
  console.log("Logged in with Account:", await signer.getAddress());
  return signer;
}


// encode into a function
function createProof(address) {
  let leaf = keccak256(address)
  let hexProof = merkleTree.getHexProof(leaf)
  return hexProof
}

function isWhiteListed(address) {
  let leaf = keccak256(address)
  let hexProof = createProof(address)
  let isValid = merkleTree.verify(hexProof, leaf, rootHash)
  return isValid
}

// mints an NFT
async function mintNFT() {
  var signer = await login()
  var address = await signer.getAddress();
  console.log("Logged in as: " + address);

  // if not whitelisted, throw error
  if (!isWhiteListed(address)) {
    console.log("Not whitelisted");
    alert("The NFT is fully minted out. Set up testnet faucets or donate to existing ones to be included in the next snapshot! <3");
    return;
  }

  // init contract
  var contractAddress = "{{ contractAddress }}"; // MAINNET
  var contract = new ethers.Contract(contractAddress, polyfaucetABI, signer);

  // create proof to submit to contract
  let proof = createProof(address)
  console.log("hexProof: " + proof);

  // submit proof to contract
  let tx = await contract.mint(proof, { gasLimit: 1000000 });
  console.log("tx.hash: " + tx.hash);
  alert("Transaction submitted, hash:\n\n " + tx.hash);
}