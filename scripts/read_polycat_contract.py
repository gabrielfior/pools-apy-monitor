polygon_address = '0x2A333B3f9833558d583A6BADaBeCd62cE7A377b8'

polycat_staking_contract_address = '0x8CFD1B9B7478E7B0422916B72d1DB6A9D513D734'

fish_per_block = 800000000000000000 # divide by qe18

'''
IERC20 lpToken;           // Address of LP token contract.
        uint256 allocPoint;       // How many allocation points assigned to this pool. FISHes to distribute per block.
        uint256 lastRewardBlock;  // Last block number that FISHes distribution occurs.
        uint256 accFishPerShare;   // Accumulated FISHes per share, times 1e18. See below.
        uint16 depositFeeBP;      // Deposit fee in basis points
'''

# pending fish for frontend
'''
if (block.number > pool.lastRewardBlock && lpSupply != 0) {
            uint256 multiplier = getMultiplier(pool.lastRewardBlock, block.number);
            uint256 fishReward = multiplier.mul(fishPerBlock).mul(pool.allocPoint).div(totalAllocPoint);
            accFishPerShare = accFishPerShare.add(fishReward.mul(1e18).div(lpSupply));
        }
        return user.amount.mul(accFishPerShare).div(1e18).sub(user.rewardDebt);
'''