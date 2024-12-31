// SPDX-License-Identifier: MIT
pragma solidity >=0.8.14;

contract Voting {
    struct Candidate {
        uint id;
        string name;
        uint votecount;
    }

    struct Voter {
        bool hasvoted;
        uint candidateid;
    }

    mapping(address => Voter) public voters;
    mapping(uint => Candidate) public candidates;
    uint public candidatescount;
    uint public votescount;

    address public owner;
    uint public startTime;
    uint public endTime;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    modifier votingPeriod() {
        require(block.timestamp + 1 minutes >= startTime && block.timestamp <= endTime, "Voting is not live");
        _;
    }

    event Candidateadded(uint id, string name);
    event voted(address voter, uint candidateid);

    constructor() {
        owner = msg.sender;
    }

    function setVotingPeriod(uint _durationMinutes) public onlyOwner {
        startTime = block.timestamp;
        endTime = block.timestamp + (_durationMinutes * 1 minutes);
    }

    function addCandidate(string memory _name) public onlyOwner {
        candidatescount++;
        candidates[candidatescount] = Candidate(candidatescount, _name, 0);
        emit Candidateadded(candidatescount, _name);
    }

    function vote(uint _candidateid) public votingPeriod {
        require(!voters[msg.sender].hasvoted, "You have already voted");
        require(_candidateid > 0 && _candidateid <= candidatescount, "Invalid candidate count");

        voters[msg.sender] = Voter(true, _candidateid);
        candidates[_candidateid].votecount++;

        emit voted(msg.sender, _candidateid);
    }

    function getCandidate(uint _candidateid) public view returns (uint, string memory name, uint) {
        require(_candidateid >= 0 && _candidateid <= candidatescount, "Invalid candidate count");
        Candidate memory candidate = candidates[_candidateid];
        return (candidate.id, candidate.name, candidate.votecount);
    }

    function GetTotals() public view returns(uint Candidates, uint Votes){
        uint totalVotes = 0;
        for (uint i = 1; i <= candidatescount; i++){
            totalVotes += candidates[i].votecount;
        }

        return (candidatescount, totalVotes);
    }

    function GetCandidateVotes() public view returns (Candidate[] memory){
        Candidate[] memory CandidateList= new Candidate[](candidatescount);  
        for (uint i = 1; i <= candidatescount; i++){
            CandidateList[i-1] = candidates[i];
        } 
        return CandidateList;
    }
}