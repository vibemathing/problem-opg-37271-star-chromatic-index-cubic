// C25: enumerate full proper six-colorings with monochromatic-palette constraints.
// This is new candidate code; no C20/C23/C24 source is imported.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <openssl/evp.h>
#include <sys/resource.h>
#include <unistd.h>
using namespace std;
struct Entry {array<uint8_t,32> costs; unsigned seen=0; Entry(){costs.fill(255);}};
struct Topo {bool valid=false,span=false,pm=false; int k=0,lmax=0;array<int,5> first{};array<unsigned,32> five{};};
int n,m;vector<pair<int,int>> edges;array<unsigned,10> incident{};array<unsigned,15> near_edge{};
vector<unsigned> shape;vector<int> penalty;vector<Topo> topology;
array<unsigned,7> cm{};array<int,15> col{};array<uint64_t,15> place{};
unordered_map<uint64_t,Entry> states;uint64_t leaves=0,nodes=0;
void require(bool b,const string &s){if(!b)throw runtime_error(s);}
string sha(EVP_MD_CTX*ctx){unsigned char bytes[32];unsigned len=0;EVP_DigestFinal_ex(ctx,bytes,&len);require(len==32,"digest");string s;const char*h="0123456789abcdef";for(auto a:bytes){s+=h[a>>4];s+=h[a&15];}return s;}
void prepare(){
 const int lim=1<<m;penalty.assign(lim,0);topology.resize(lim);
 for(int mask=0;mask<lim;++mask){
  if(__builtin_popcount((unsigned)mask)==4){array<int,10> deg{};unsigned V=0;for(int e=0;e<m;++e)if(mask>>e&1){auto [a,b]=edges[e];++deg[a];++deg[b];V|=(1u<<a)|(1u<<b);}
   int ones=0,twos=0;for(int v=0;v<n;++v){ones+=deg[v]==1;twos+=deg[v]==2;}
   if((ones==2&&twos==3)||(ones==0&&twos==4)){
    unsigned reached=1u<<__builtin_ctz(V),old=0;while(reached!=old){old=reached;for(int e=0;e<m;++e)if(mask>>e&1){auto [a,b]=edges[e];if((reached>>a&1)||(reached>>b&1))reached|=(1u<<a)|(1u<<b);}}
    if(reached==V){shape.push_back(mask);penalty[mask]=1;}
   }
  }
  Topo &t=topology[mask];unsigned todo=mask,Vall=0;array<int,10> deg{};for(int e=0;e<m;++e)if(mask>>e&1){++deg[edges[e].first];++deg[edges[e].second];}
  bool ok=true;for(int v=0;v<n;++v)if(deg[v]>2)ok=false;
  if(!ok)continue;
  array<unsigned,5> even{},odd{};
  while(todo&&ok){int seed=__builtin_ctz(todo);unsigned component=1u<<seed,old=0;while(component!=old){old=component;for(int e=0;e<m;++e)if(component>>e&1)component|=near_edge[e]&mask;}
   int len=__builtin_popcount(component);if(len>3||t.k==5){ok=false;break;}
   unsigned V=0;for(int e=0;e<m;++e)if(component>>e&1)V|=(1u<<edges[e].first)|(1u<<edges[e].second);
   int start=-1,ends=0;for(int v=0;v<n;++v)if((V>>v&1)&&deg[v]==1){if(start<0)start=v;++ends;}
   if(ends!=2||__builtin_popcount(V)!=len+1){ok=false;break;}
   unsigned rem=component;int at=start,p=0;while(rem){unsigned next=incident[at]&rem;require(__builtin_popcount(next)==1,"path walk");int e=__builtin_ctz(next);if(!p)t.first[t.k]=e;(p%2?odd[t.k]:even[t.k])|=1u<<e;at=edges[e].first^edges[e].second^at;rem^=1u<<e;++p;}
   t.lmax=max(t.lmax,len);++t.k;todo^=component;Vall|=V;
  }
  if(!ok)continue;t.valid=true;t.span=Vall==((1u<<n)-1);t.pm=t.span&&__builtin_popcount((unsigned)mask)*2==n;
  for(int s=0;s<(1<<t.k);++s){unsigned b=0;for(int j=0;j<t.k;++j)b|=(s>>j&1)?odd[j]:even[j];t.five[s]=b;}
 }
 for(int bit=0;bit<m;++bit)for(int mask=0;mask<lim;++mask)if(mask>>bit&1)penalty[mask]+=penalty[mask^(1<<bit)];
}
void extend(int e,int used,uint64_t code){
 ++nodes;
 if(e==m){++leaves;unsigned U=cm[5]|cm[6];const Topo&t=topology[U];require(t.valid,"B premise");int phase=0;for(int i=0;i<t.k;++i)if(col[t.first[i]]==6)phase|=1<<i;
  int cost=0;for(int a=1;a<=4;++a)for(int b=5;b<=6;++b)cost+=penalty[cm[a]|cm[b]];require(cost<255,"cost cap");
  Entry&r=states[code];require(!(r.seen&(1u<<phase)),"duplicate phase");r.seen|=1u<<phase;r.costs[phase]=cost;return;
 }
 unsigned bit=1u<<e;
 for(int c=1;c<=6;++c){if(c<=4&&c>used+1)continue;if(cm[c]&near_edge[e])continue;
  cm[c]|=bit;bool ok=true;
  if(c<=4){for(int d=1;d<=4;++d)if(d!=c&&penalty[cm[c]|cm[d]]){ok=false;break;}}
  else if(penalty[cm[5]|cm[6]])ok=false;
  if(ok){col[e]=c;extend(e+1,c<=4?max(used,c):used,code+(c<=4?c*place[e]:0));}
  cm[c]^=bit;
 }
}
int main(){try{
 alarm(35);rlimit cpu{30,31},mem{805306368,805306368};setrlimit(RLIMIT_CPU,&cpu);setrlimit(RLIMIT_AS,&mem);
 require(bool(cin>>n>>m)&&n>=0&&n<=10&&m>=0&&m<=15,"input size");
 for(int e=0;e<m;++e){int a,b;require(bool(cin>>a>>b)&&a>=0&&b>=0&&a<n&&b<n&&a<b,"input edge");require(find(edges.begin(),edges.end(),make_pair(a,b))==edges.end(),"duplicate edge");edges.emplace_back(a,b);incident[a]|=1u<<e;incident[b]|=1u<<e;}
 for(int v=0;v<n;++v)require(__builtin_popcount(incident[v])<=3,"degree cap");
 for(int e=0;e<m;++e)near_edge[e]=(incident[edges[e].first]|incident[edges[e].second])^(1u<<e);
 uint64_t p=1;for(int e=m-1;e>=0;--e){place[e]=p;p*=5;}
 prepare();states.reserve(1000000);extend(0,0,0);
 vector<uint64_t> order;order.reserve(states.size());for(const auto &r:states)order.push_back(r.first);sort(order.begin(),order.end());
 struct US{uint64_t count=0,good=0,first=0;int phase=-1,minimum=255;};vector<US> us(1<<m);array<uint64_t,256> histogram{};uint64_t raw=0,rawphase=0,balanced=0,span2=0,pmgood=0;
 auto*ctx=EVP_MD_CTX_new();EVP_DigestInit_ex(ctx,EVP_sha256(),nullptr);const char*hex="0123456789abcdef";
 for(auto code:order){auto&r=states.at(code);array<int,15>w{};unsigned U=0;int q=0;for(int e=0;e<m;++e){w[e]=(code/place[e])%5;if(!w[e])U|=1u<<e;else q=max(q,w[e]);}
  const Topo&t=topology[U];int phases=1<<t.k;unsigned all=phases==32?0xffffffffu:((1u<<phases)-1);require(r.seen==all,"phase coverage");int best=255,bp=-1;string line=to_string(code)+":";
  for(int s=0;s<phases;++s){int c=r.costs[s];require(c<255,"missing phase");if(c<best){best=c;bp=s;}line+=hex[c>>4];line+=hex[c&15];}line+='\n';EVP_DigestUpdate(ctx,line.data(),line.size());
  ++histogram[best];uint64_t mult=1;for(int i=0;i<q;++i)mult*=4-i;raw+=mult;rawphase+=mult*phases;
  US&z=us[U];++z.count;z.minimum=min(z.minimum,best);if(best==0){++balanced;++z.good;if(z.phase<0){z.first=code;z.phase=bp;}span2+=t.span&&t.lmax<=2;pmgood+=t.pm;}
 }
 string digest=sha(ctx);EVP_MD_CTX_free(ctx);
 cout<<"{\"verdict\":\"candidate_only\",\"engine\":\"full-six-color\",\"n\":"<<n<<",\"m\":"<<m<<",\"frames\":"<<states.size()<<",\"raw_frames\":"<<raw<<",\"phases\":"<<leaves<<",\"raw_phases\":"<<rawphase<<",\"balanced\":"<<balanced<<",\"balanced_spanning_short2\":"<<span2<<",\"balanced_perfect_U\":"<<pmgood<<",\"nodes\":"<<nodes<<",\"shape_count\":"<<shape.size()<<",\"stream_sha256\":\""<<digest<<"\",\"mu_histogram\":{";
 bool comma=false;for(int v=0;v<256;++v)if(histogram[v]){if(comma)cout<<',';cout<<'\"'<<v<<"\":"<<histogram[v];comma=true;}cout<<"},\"U_rows\":[";
 comma=false;for(int u=0;u<(1<<m);++u)if(topology[u].valid){const auto&z=us[u];if(comma)cout<<',';cout<<'['<<u<<','<<z.count<<','<<z.good<<','<<(z.count?z.minimum:-1)<<','<<z.first<<','<<z.phase<<']';comma=true;}cout<<"]}\n";
 }catch(const exception&e){cerr<<e.what()<<'\n';return 2;}}
