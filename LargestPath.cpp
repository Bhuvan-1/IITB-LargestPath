#include<bits/stdc++.h>
using namespace std;

int N;
int NUM_EDGES;
vector<int>* ADJ;
unordered_map<int, string> vertex_name;
int** ADJ_MATRIX;


typedef pair<int,vector<int>> pv;


pv MAX_PATH(int v){
    int w;
    int max_path = 0;
    vector<int> ret;
    for(auto i : ADJ[v]){
        if(ADJ_MATRIX[v][i] != -1){
            w = ADJ_MATRIX[v][i];
            ADJ_MATRIX[v][i] = -1;
            ADJ_MATRIX[i][v] = -1;
            pv p = MAX_PATH(i);
            if(p.first + w > max_path){
                max_path = p.first + w;
                ret = p.second;
            }
            ADJ_MATRIX[v][i] = w;
            ADJ_MATRIX[i][v] = w;
        }
    }
    ret.push_back(v);
    return {max_path,ret};
}

void validate_route(vector<int> route){
    vector<vector<bool>> visited(N+1,vector<bool>(N+1,false));
    int n = route.size();
    int sum = 0;
    for(int i = n-1; i > 0; i--){
        int a,b;
        a = route[i];
        b = route[i-1];
        if(visited[a][b]){
            cout << "Invalid Route!, " << a << " to " << b << " Repeated" << endl;
            return;
        }
        else{
            visited[a][b] = visited[b][a] = true;
        }
        sum += ADJ_MATRIX[a][b];
        cout << ADJ_MATRIX[a][b] << " : " << vertex_name[a] << "(" << a << ") -> (" << b << ")" << vertex_name[b] << endl;
    }

    cout << "Total Edges : " << n-1 << endl;
    cout << "Total Calculated Distance : " << sum << endl;

}


int main(){
    cin >> N;
    ADJ = new vector<int>[N+1];
    ADJ_MATRIX = new int*[N+1];
    for(int i = 0; i <= N; i++){
        ADJ_MATRIX[i] = new int[N+1];
        for(int j = 0; j <= N; j++){
            ADJ_MATRIX[i][j] = -1;
        }
    }
    int u,v,w;
    string s;
    while(true){
        cin >> v >> s;
        if(v == -1) break;
        vertex_name[v] = s;
    }

    while(cin >> u >> v >> w){
        ADJ[u].push_back(v);
        ADJ[v].push_back(u);
        ADJ_MATRIX[u][v] = w;
        ADJ_MATRIX[v][u] = w;
        NUM_EDGES++;
    }

    int max_path = 0;
    int start_vertex = 0;
    vector<int> route;
    for(int i = 1; i <= N; i++){
        pv p = MAX_PATH(i);
        if(p.first > max_path){
            max_path = p.first;
            route = p.second;
            start_vertex = i;
        }
    }

    validate_route(route);

    cout << "Start Vertex: " << vertex_name[start_vertex] << endl;
    cout << "Max Path: " << (max_path/1000.0)  << "Km" << endl;


}