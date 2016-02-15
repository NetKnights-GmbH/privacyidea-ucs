/**
 * http://www.privacyidea.org
 * (c) cornelius kölbel, cornelius@privacyidea.org
 *
 * 2015-04-17 Cornelius Kölbel, <cornelius.koelbel@netknights.it>
 *
 * This code is free software; you can redistribute it and/or
 * modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 * License as published by the Free Software Foundation; either
 * version 3 of the License, or any later version.
 *
 * This code is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU AFFERO GENERAL PUBLIC LICENSE for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */
myApp.controller("systemAddonController", function ($scope, $location,
                                               $rootScope, $state, inform,
                                               AuthFactory, $upload, $http,
                                               instanceUrl) {
    $scope.upload = function (files) {
        if (files && files.length) {
            for (var i = 0; i < files.length; i++) {
                var file = files[i];
                $upload.upload({
                    url: instanceUrl + '/subscription/',
                    headers: {'Authorization': AuthFactory.getAuthToken()},
                    fields: {filename: "somename"},
                    file: file
                }).success(function (data, status, headers, config) {
                    $scope.get_subscription();
                }).error(function (error) {
                    if (error.result.error.code == -401) {
                        $state.go('login');
                    } else {
                        inform.add(error.result.error.message,
                                    {type: "danger", ttl: 10000});
                    }
                });
            }
        }
    };

    $scope.get_subscription = function () {
        $http.get(instanceUrl + "/subscription", {
            headers: {'Authorization': AuthFactory.getAuthToken()}
            }).success(function(data){
                $scope.subscription = data.result.value;
            }
            ).error(function (error) {
            if (error.result.error.code == -401) {
                $state.go('login');
            } else {
                inform.add(error.result.error.message,
                            {type: "danger", ttl: 10000});
            }
        });
    };

    $scope.get_subscription();

});
