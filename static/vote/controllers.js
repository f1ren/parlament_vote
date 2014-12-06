voteModule.controller('voteController', ['$scope', '$http', function($scope, $http) {
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
    
    $scope.vote = {};
    $scope.jobs.forEach(function(job) {
    	$scope.vote[job] = [''];
    });
    $scope.persons = [
    	"בוז'י הרצוג",
    ];

    $scope.addCandidate = function(candidates) {
    	if (candidates.length < 3) candidates.push('');
    };

	$scope.removeCandidate = function(candidates) {
    	if (candidates.length > 1) candidates.pop();
    };

    $scope.send = function() {
        $http.post("http://127.0.0.1:8000/post/", $scope.vote).
        success(function(data, status, headers, config) {
            console.log(data);
        }).
        error(function(data, status, headers, config) {
        });
    }
}]);