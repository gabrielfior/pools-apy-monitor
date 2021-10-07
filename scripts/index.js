
const Web3 = require("web3");
const fs = require("fs");

var web3 = new Web3("https://bsc-dataseed1.binance.org:443");
const BNObject = Web3.utils.BN;
const BN = (x) => new BNObject(x);

const ABIjson = fs.readFileSync("../contracts/pancakeswapContract.json"); // pool contract
const ABIjsonAutoRestaking = fs.readFileSync("../contracts/pancakeswapContract.json"); // pool autorestaking contract
const CakeABIJson = fs.readFileSync("../contracts/cakeContract.json"); //cake contract
const ABI = JSON.parse(ABIjson);
const CakeABI = JSON.parse(CakeABIJson);

const contractAdd = "0x73feaa1eE314F8c655E354234017bE2193C9E24E";
const cakeContractAdd = "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82";

async function pancakeAPR() {
  const contract = new web3.eth.Contract(ABI, contractAdd);
  const poolInfo = await contract.methods.poolInfo("0").call();
  const allocPoints = poolInfo.allocPoint;
  console.log('poolInfo', poolInfo);
  
  let result = await contract.methods.cakePerBlock().call();
  console.log('cake per block', result);
  const cakePerBlock = BN(result);

  console.log('cake per block', result);
  const poolAllocPoint = BN(allocPoints);
  
  result = await contract.methods.totalAllocPoint().call();
  console.log('totalAllocPoints', result);
  const totalAllocPoint = BN(result);

  const blockReward = cakePerBlock.mul(poolAllocPoint).div(totalAllocPoint);
  console.log('blockReward', blockReward.toString());
  const numberOfBlocks = 20 * 60 * 24 * 365;
  console.log('numberOfBlocks', numberOfBlocks);
  const annualBlockReward = blockReward
    .mul(BN(numberOfBlocks.toString()))
    .mul(BN("1000000000000"));
console.log('annual block reward', annualBlockReward.toString());

  const cakeContract = new web3.eth.Contract(CakeABI, cakeContractAdd);
  console.log('contract.options.address', contract.options.address);
  result = await cakeContract.methods
    .balanceOf(contract.options.address)
    .call();
    console.log('lp supply', result);
  const lpSupply = BN(result);
  const apr =
    annualBlockReward.div(lpSupply).divRound(BN("100000000")).toNumber() / 100;
  return apr;
}

const x = pancakeAPR().then((value) => console.log(value));