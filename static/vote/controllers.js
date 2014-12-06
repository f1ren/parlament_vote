voteModule.controller('voteController', ['$scope', '$http', '$location', function($scope, $http, $location) {
    $scope.sending = false;
    $scope.sent = false;
    $scope.jobs = [
        "ראש הממשלה",
        "שר האוצר",
        "שר הביטחון",
        "שר החינוך",
        "שר המשפטים",
        "שר הכלכלה",
        "שר התחבורה",
        "שר החוץ",
        "שר הפנים",
        "שר המדע",
        "שר החקלאות",
        "שר התרבות והספורט",
        "שר הבריאות",
        "שר לביטחון פנים",
        "שר התקשורת",
        "שר הבינוי והשיכון",
        "שר הגנת הסביבה",
        "שר התיירות",
        "מבקר המדינה",
        ];
    
    var givenVote = $location.search().vote;
    if (angular.isDefined(givenVote)) {
        $scope.vote = angular.fromJson(givenVote);
    } else {
        $scope.vote = {};
        $scope.jobs.forEach(function(job) {
            $scope.vote[job] = [{name: ''}];
        });
    }
    
    $scope.candidates = [];
    $http.get("/candidates/", $scope.vote).
        success(function(data, status, headers, config) {
            data.forEach(function(candidate) {
                $scope.candidates.push(candidate);
            });
        }).
        error(function(data, status, headers, config) {
        });

    $scope.addCandidate = function(candidates) {
    	if (candidates.length >= 3) return;
        if (candidates.indexOf({name: ''}) > -1) return;
        candidates.push({name: ''});
    };

	$scope.removeCandidate = function(candidates) {
    	if (candidates.length <= 1) return;
        candidates.pop();
    };

    $scope.send = function() {
        $scope.sending = true;
        $scope.shareLink = '#/?vote=' + angular.toJson($scope.vote);
        $http.post("/post/", $scope.vote).
        success(function(data, status, headers, config) {
            $scope.sending = false;
            $scope.sent = true;
        }).
        error(function(data, status, headers, config) {
            $scope.sending = false;
            $scope.sent = true;
        });
    }
}]);