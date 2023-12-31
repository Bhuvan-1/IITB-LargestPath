#include <bits/stdc++.h>
using namespace std;


void dfs(vector<int>* ADJ, int* visited, int N, int count, int v){
    visited[v] = count;
    for(auto w : ADJ[v]){
        if(visited[w] == 0){
            dfs(ADJ, visited, N, count, w);
        }
    }
}


int main(int argc, char* argv[]){

    if(argc != 2){
        cout << "Invalid number of arguments, Usage: ./a.out [1/2/3] < output.txt" << endl;
        return 0;
    }
    int choice = atoi(argv[1]);


    int n;
    cin >> n;

    vector<int> ADJ[n+1];
    int start;
    int end;

    int i, j;
    while(true){
        cin >> i;
        if(i == -1) break;
        cin >> j;
        ADJ[i].push_back(j);
        ADJ[j].push_back(i);
    }

    if(choice == 3){
        cin >> start;
        cin >> end;
    }


    int visited[n+1];
    for(int i = 0; i <= n; i++){
        visited[i] = 0;
    }

    int count = 1;
    for(int i = 1; i <= n; i++){
        if(ADJ[i].size() == 0){
            visited[i] = -1;
        }
        else if(visited[i] == 0){
            dfs(ADJ, visited, n, count, i);
            count++;
        }
    }

    if(count == 2){
        cout << "Valid closed path" << endl;
    }
    else{
        cout << "Invalid Closed path: Found " << count-1 << "components" << endl;
        return 0;
    }


        //Sample Walk
        int v;
        if(choice == 1 || choice == 2){
            for(int i = 1; i <= n; i++){
                if(ADJ[i].size() > 0){
                    v = i;
                    break;
                }
            }
        }
        else{
            v = start;
            cout << "Start: " << v << endl;
            cout << "End: " << end << endl;
        }



        cout << v << " ";
        while(ADJ[v].size() != 0){
            int w = ADJ[v][0];
            cout << w << " ";
            count++;
            ADJ[v].erase(ADJ[v].begin());
            ADJ[w].erase(find(ADJ[w].begin(), ADJ[w].end(), v));
            v = w;
        }
        cout << endl;

}