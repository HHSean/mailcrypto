

const provider = new ethers.providers.Web3Provider(window.ethereum, "any");

// switch to Polygon
let web3 = window.ethereum;
web3
  .request({
    method: "wallet_switchEthereumChain",
    params: [{ chainId: "0x13881" }]
  })
  .catch(() => { });

async function main() {
}


async function login() {
  // Prompt user for account connections
  await provider.send("eth_requestAccounts", []);
  const signer = provider.getSigner();
  console.log("Logged in with Account:", await signer.getAddress());
  return signer;
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